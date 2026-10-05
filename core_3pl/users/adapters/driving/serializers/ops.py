from config.serializers import BaseModelSerializer
from rest_framework import serializers

from users.models import Ops


class OpsRegisterSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Ops
        fields = "__all__"
        read_only_fields = BaseModelSerializer.Meta.read_only_fields + ["user"]


class OpsGetSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    user = serializers.UUIDField(source="user_id")
    full_name = serializers.CharField()
    department = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()