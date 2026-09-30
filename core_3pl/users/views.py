from config.permission import IsOps
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .domain.enums import Role
from .models import Ops, Tenant, User
from .serializers import (
    OpsGetSerializer,
    OpsRegisterSerializer,
    TenantGetSerializer,
    TenantRegisterSerializer,
    UserGetSerializer,
    UserRegisterSerializer,
)


class RegisterUser(APIView):
    def post(self, request):
        role = request.data.get("role")
        user_serializer = UserRegisterSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        if role == Role.OPS:
            profile_serializer = OpsRegisterSerializer(data=request.data)
        elif role == Role.TENANT:
            profile_serializer = TenantRegisterSerializer(data=request.data)
        else:
            return Response(
                {"role": "invalid role"}, status=status.HTTP_400_BAD_REQUEST
            )

        profile_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = user_serializer.save()
            profile_serializer.save(user=user)

        return Response(UserGetSerializer(user).data, status=status.HTTP_201_CREATED)


class ListUsers(APIView):
    permission_classes = (IsOps,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)


class ListTenants(APIView):
    permission_classes = (IsOps,)

    def get(self, request):
        users = Tenant.objects.all()
        serializer = TenantGetSerializer(users, many=True)
        return Response(serializer.data)


class ListOps(APIView):
    permission_classes = (IsOps,)

    def get(self, request):
        users = Ops.objects.all()
        serializer = OpsGetSerializer(users, many=True)
        return Response(serializer.data)
