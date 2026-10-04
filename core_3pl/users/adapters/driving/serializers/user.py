from config.serializers import BaseModelSerializer
from rest_framework import serializers

from users.models import User


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
        exclude = ("password",)