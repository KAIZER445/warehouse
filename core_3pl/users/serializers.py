from rest_framework import serializers
from .models import User, Tenant, Ops
from config.serializers import BaseModelSerializer


class UserRegisterSerializer(BaseModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta(BaseModelSerializer.Meta):
        model = User
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["is_active"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]

# ------------------------------------------------------------

class TenantRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Tenant
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["user"]


class TenantGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"

# ------------------------------------------------------------

class OpsRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Ops
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["user"]


class OpsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ops
        fields = "__all__"
