from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserGetSerializer, UserRegisterSerializer, TenantRegisterSerializer, OpsRegisterSerializer
from rest_framework import status
from .enums import Role
from django.db import transaction

class RegisterUser(APIView):
    def post(self, request):
        role = request.data.get("role")
        user_serializer = UserRegisterSerializer(data =request.data)
        user_serializer.is_valid(raise_exception=True)

        if role == Role.OPS:
            profile_serializer = OpsRegisterSerializer(data = request.data)
        elif role == Role.TENANT:
            profile_serializer = TenantRegisterSerializer(data = request.data)
        else:
            return Response({"role": "invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        profile_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = user_serializer.save()
            profile_serializer.save(user = user)
        
        return Response(UserGetSerializer(user).data, status=status.HTTP_201_CREATED)

class ListUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserGetSerializer(users, many= True)
        return Response(serializer.data)