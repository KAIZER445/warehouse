from config.permission import IsOps
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Tenant
from users.core.application.services import TenantService
from users.core.domain.ports import TenantServicePort
from users.adapters.driven.repositories import TenantRepository
from users.adapters.driving.serializers import TenantGetSerializer
from rest_framework import status


class ListTenants(APIView):
    permission_classes = (IsOps,)

    def get(self, request):
        tenants = Tenant.objects.all()
        serializer = TenantGetSerializer(tenants, many=True)
        return Response(serializer.data)


class DeactivateTenant(APIView):
    permission_classes = [IsOps]
    service: TenantServicePort = TenantService(TenantRepository())

    def post(self, request, tenant_id):
        try:
            self.service.deactivate(tenant_id)
        except Tenant.DoesNotExist:
            return Response({"error": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=409)
        return Response(status=204)