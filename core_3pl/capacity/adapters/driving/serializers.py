from decimal import Decimal
from rest_framework import serializers
from capacity.models import Capacity as CapacityModel
from capacity.core.domain.enums import Operators

class CapacityGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapacityModel
        fields = "__all__"

class AllocatedSpaceSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=14, decimal_places=5, min_value=Decimal("0.00001"))
    operation = serializers.ChoiceField(choices=Operators.choices)