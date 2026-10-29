from rest_framework import serializers
from lease.models import Lease as LeaseModel
from decimal import Decimal

class LeaseGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseModel
        fields = "__all__"

class CreateQuoteSerializer(serializers.Serializer):
    tenant_id = serializers.IntegerField()
    box_combination = serializers.JSONField()
    total_boxes = serializers.IntegerField()
    minimum_required_space = serializers.DecimalField()
    total_volume = serializers.DecimalField()
    total_weight = serializers.DecimalField()

class BookInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    format_type = serializers.CharField(max_length=50)
    length = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal("0.01"))
    width = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal("0.01"))
    thickness = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal("0.01"))
    unit_weight = serializers.DecimalField(max_digits=8, decimal_places=3, min_value=Decimal("0.001"))
    quantity = serializers.IntegerField(min_value=1)
