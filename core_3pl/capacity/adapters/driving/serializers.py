from rest_framework import serializers
from capacity.models import Capacity as CapacityModel

class CapacityGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacityModel
        fields = "__all__"