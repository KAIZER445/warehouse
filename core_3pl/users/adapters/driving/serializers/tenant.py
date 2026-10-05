from config.serializers import BaseModelSerializer
from rest_framework import serializers

from users.models import Tenant


class TenantRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Tenant
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["user"]


class TenantGetSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.UUIDField(source="user_id")
    company_name = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()