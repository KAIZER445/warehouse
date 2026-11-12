from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Tenant, Ops
from lease.models import Lease
from lease.core.domain.enum import LeaseStatus


class UserEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_tenant_registration(self):
        res = self.client.post("/user/register/", {
            "email": "t_test@example.com",
            "password": "Password123!",
            "role": "tenant",
            "company_name": "Test Company",
            "base_url": "https://testcompany.example.com",
            "encrypted_secret": "test_hmac_secret_123"
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="t_test@example.com").exists())
        tenant = Tenant.objects.filter(company_name="Test Company").first()
        self.assertIsNotNone(tenant)
        self.assertEqual(tenant.base_url, "https://testcompany.example.com")
        self.assertEqual(tenant.encrypted_secret, "test_hmac_secret_123")

    def test_ops_registration(self):
        res = self.client.post("/user/register/", {
            "email": "o_test@example.com",
            "password": "Password123!",
            "role": "ops",
            "full_name": "Operator Joe",
            "department": "customer_support"
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="o_test@example.com").exists())
        self.assertTrue(Ops.objects.filter(full_name="Operator Joe").exists())

    def test_jwt_auth_and_user_listing(self):
        # Register Ops
        self.client.post("/user/register/", {
            "email": "ops_list@example.com",
            "password": "Password123!",
            "role": "ops",
            "full_name": "List Operator",
            "department": "capacity_management"
        }, format="json")
        # Token
        tok_res = self.client.post("/api/token/", {
            "email": "ops_list@example.com",
            "password": "Password123!"
        }, format="json")
        self.assertEqual(tok_res.status_code, status.HTTP_200_OK)
        token = tok_res.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        list_res = self.client.get("/user/list/")
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)

    def test_tenant_deactivation_guard(self):
        # Register Ops
        self.client.post("/user/register/", {
            "email": "ops_deact@example.com",
            "password": "Password123!",
            "role": "ops",
            "full_name": "Deact Ops",
            "department": "customer_support"
        }, format="json")
        tok_res = self.client.post("/api/token/", {
            "email": "ops_deact@example.com",
            "password": "Password123!"
        }, format="json")
        ops_token = tok_res.data["access"]

        # Register Tenant
        self.client.post("/user/register/", {
            "email": "tenant_lease@example.com",
            "password": "Password123!",
            "role": "tenant",
            "company_name": "Leased Co",
            "base_url": "https://leasedco.example.com",
            "encrypted_secret": "leased_co_secret_456"
        }, format="json")
        tenant = Tenant.objects.get(company_name="Leased Co")

        # Create active lease
        Lease.objects.create(
            tenant=tenant,
            box_combination={"SMALL": 1},
            total_boxes=1,
            minimum_required_space=12000,
            total_volume=10000,
            total_weight=5,
            status=LeaseStatus.ACTIVE
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {ops_token}")
        deact_res = self.client.post(f"/user/tenants/{tenant.id}/deactivate/")
        self.assertEqual(deact_res.status_code, status.HTTP_409_CONFLICT)

    def test_list_tenants(self):
        # Register Ops
        self.client.post("/user/register/", {
            "email": "ops_list_t@example.com",
            "password": "Password123!",
            "role": "ops",
            "full_name": "Tenant List Ops",
            "department": "customer_support"
        }, format="json")
        tok_res = self.client.post("/api/token/", {
            "email": "ops_list_t@example.com",
            "password": "Password123!"
        }, format="json")
        ops_token = tok_res.data["access"]

        # Register Tenant
        self.client.post("/user/register/", {
            "email": "listed_tenant@example.com",
            "password": "Password123!",
            "role": "tenant",
            "company_name": "Listed Tenant Inc",
            "base_url": "https://listed.example.com",
            "encrypted_secret": "sensitive_hmac_secret"
        }, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {ops_token}")
        res = self.client.get("/user/list/tenants/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tenants = res.data
        self.assertTrue(any(t["company_name"] == "Listed Tenant Inc" for t in tenants))
        matched = next(t for t in tenants if t["company_name"] == "Listed Tenant Inc")
        self.assertEqual(matched["base_url"], "https://listed.example.com")
        self.assertNotIn("encrypted_secret", matched)
