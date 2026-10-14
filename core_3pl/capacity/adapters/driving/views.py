from django.shortcuts import render
from rest_framework.views import APIView
from config.permission import IsOps
from capacity.core.domain.ports_service import CapacityServicePort
from capacity.adapters.driven.repositories import CapacityRepository
from .serializers import CapacityGetSerializer, AllocatedSpaceSerializer
from rest_framework.response import Response
from capacity.core.application.services import CapacityService


class GetCapacity(APIView):
    permission_classes = (IsOps,)
    service: CapacityServicePort = CapacityService(CapacityRepository())

    def get(self, request):
        capacity = self.service.get_capacity()
        serializer = CapacityGetSerializer(capacity)
        return Response(serializer.data)


class UpdateAllocatedSpace(APIView):
    permission_classes = (IsOps,)
    service: CapacityServicePort = CapacityService(CapacityRepository())

    def patch(self, request):
        serilaizer = AllocatedSpaceSerializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)

        try:
            self.service.update_allocated_space(
                serilaizer.validated_data["amount"],
                serilaizer.validated_data["operation"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(status=204)
