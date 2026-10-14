from rest_framework import serializers
from capacity.models import Capacity as CapacityModel
from capacity.core.domain.enums import Operators

class CapacityGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacityModel
        fields = "__all__"

class AllocatedSpaceSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)
    operation = serializers.ChoiceField(choices=Operators.choices)