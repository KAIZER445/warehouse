from config.permission import IsOps
from rest_framework.response import Response
from rest_framework.views import APIView

from users.core.domain.ports import OpsServicePort
from users.core.application.services import OpsService
from users.adapters.driven.repositories import OpsRepository
from ..serializers.ops import OpsGetSerializer


class ListOps(APIView):
    permission_classes = (IsOps,)
    service: OpsServicePort = OpsService(OpsRepository())

    def get(self, request):
        ops = self.service.list_all()
        serializer = OpsGetSerializer(ops, many=True)
        return Response(serializer.data)