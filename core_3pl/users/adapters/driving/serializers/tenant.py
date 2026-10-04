from config.serializers import BaseModelSerializer
from rest_framework import serializers

from users.models import Tenant


class TenantRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Tenant
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["user"]


class TenantGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"