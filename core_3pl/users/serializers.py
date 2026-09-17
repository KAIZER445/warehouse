from rest_framework import serializers
from .models import User, Tenant, Ops
from config.serializers import BaseModelSerializer

class UserRegisterSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["role", "is_active"]
        extra_kwargs = {"password": {"write_only": True}}


class TenantRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Tenant
        fields = "__all__"


class OpsRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Ops
        fields = "__all__"