from config.permission import IsOps
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.core.domain.enums import Role
from users.core.domain.ports import UserServicePort
from users.core.application.services import UserService
from users.adapters.driven.repositories import UserRepository, TenantRepository, OpsRepository
from ..serializers.user import UserGetSerializer, UserRegisterSerializer
from ..serializers.tenant import TenantRegisterSerializer
from ..serializers.ops import OpsRegisterSerializer


class RegisterUser(APIView):
    service: UserServicePort = UserService(
        UserRepository(), TenantRepository(), OpsRepository()
    )

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
            user = self.service.register(
                email=user_serializer.validated_data["email"],
                password=user_serializer.validated_data["password"],
                role=role,
                profile_data=profile_serializer.validated_data,
            )

        return Response(UserGetSerializer(user).data, status=status.HTTP_201_CREATED)


class ListUsers(APIView):
    permission_classes = (IsOps,)
    service: UserServicePort = UserService(
        UserRepository(), TenantRepository(), OpsRepository()
    )

    def get(self, request):
        users = self.service.list_all()
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data)