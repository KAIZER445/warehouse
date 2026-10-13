from django.shortcuts import render
from rest_framework.views import APIView
from config.permission import IsOps
from capacity.core.domain.ports_service import CapacityServicePort
from capacity.core.domain.ports import Capacity as CapacityPort
from capacity.adapters.driven.repositories import CapacityRepository
from .serializers import CapacityGetSerializer
from rest_framework.response import Response
from capacity.core.application.services import CapacityService

class GetCapacity(APIView):
    permission_classes = (IsOps,)
    service: CapacityServicePort = CapacityService(CapacityRepository())

    def get(self, request):
        capacity = self.service.get_capacity()
        serializer = CapacityGetSerializer(capacity)
        return Response(serializer.data)