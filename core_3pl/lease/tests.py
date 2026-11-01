from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Tenant


class LeaseEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post("/user/register/", {
            "email": "lease_tenant@example.com",
            "password": "Password123!",
            "role": "tenant",
            "company_name": "Lease Test Co"
        }, format="json")
        tok_res = self.client.post("/api/token/", {
            "email": "lease_tenant@example.com",
            "password": "Password123!"
        }, format="json")
        self.token = tok_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_quote_and_activation(self):
        # 1. Create Quote
        res = self.client.post("/lease/create-quote/", {
            "books": [
                {
                    "title": "Clean Code",
                    "author": "Robert C. Martin",
                    "format_type": "Hardcover",
                    "length": "23.50",
                    "width": "17.80",
                    "thickness": "3.00",
                    "unit_weight": "0.650",
                    "quantity": 100
                }
            ]
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        lease_id = res.data["lease_id"]
        min_space = Decimal(res.data["minimum_required_space"])
        self.assertEqual(res.data["status"], "PENDING")

        # 2. Reject activation below min_space
        res_low = self.client.post(f"/lease/{lease_id}/activate/", {
            "selected_space": str(min_space - Decimal("1.00")),
            "term_months": 12,
            "start_date": "2026-11-15"
        }, format="json")
        self.assertEqual(res_low.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. Reject activation above 3x min_space
        res_high = self.client.post(f"/lease/{lease_id}/activate/", {
            "selected_space": str(round(min_space * Decimal("3.1"), 2)),
            "term_months": 12,
            "start_date": "2026-11-15"
        }, format="json")
        self.assertEqual(res_high.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. Successful activation
        res_ok = self.client.post(f"/lease/{lease_id}/activate/", {
            "selected_space": str(min_space * Decimal("2")),
            "term_months": 6,
            "start_date": "2026-11-15"
        }, format="json")
        self.assertEqual(res_ok.status_code, status.HTTP_200_OK)
        self.assertEqual(res_ok.data["status"], "ACTIVE")
