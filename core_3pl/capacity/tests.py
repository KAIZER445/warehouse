from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User, Ops
from capacity.models import Capacity


class CapacityEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.capacity = Capacity.objects.create(
            total_capacity=Decimal("100000.00000"),
            current_allocated_space=Decimal("1000.00000")
        )
        # Register and auth ops user
        self.client.post("/user/register/", {
            "email": "ops_cap@example.com",
            "password": "Password123!",
            "role": "ops",
            "full_name": "Cap Ops",
            "department": "capacity_management"
        }, format="json")
        tok_res = self.client.post("/api/token/", {
            "email": "ops_cap@example.com",
            "password": "Password123!"
        }, format="json")
        token = tok_res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_capacity(self):
        res = self.client.get("/capacity/get/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(res.data["total_capacity"]), Decimal("100000.00000"))

    def test_update_allocated_space_addition(self):
        res = self.client.patch("/capacity/update-allocated-space/", {
            "amount": "500.00000",
            "operation": "addition"
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.capacity.refresh_from_db()
        self.assertEqual(self.capacity.current_allocated_space, Decimal("1500.00000"))

    def test_update_allocated_space_subtraction(self):
        res = self.client.patch("/capacity/update-allocated-space/", {
            "amount": "500.00000",
            "operation": "subtraction"
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.capacity.refresh_from_db()
        self.assertEqual(self.capacity.current_allocated_space, Decimal("500.00000"))
