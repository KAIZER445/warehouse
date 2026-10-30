from rest_framework import serializers
from lease.models import Lease as LeaseModel
from decimal import Decimal

class LeaseGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaseModel
        fields = "__all__"

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

class CreateQuoteSerializer(serializers.Serializer):
    books = BookInputSerializer(many=True, allow_empty=False)

class QuoteResponseSerializer(serializers.Serializer):
    lease_id = serializers.UUIDField()
    status = serializers.CharField()
    minimum_required_space = serializers.DecimalField(max_digits=20, decimal_places=2)
    box_combination = serializers.JSONField()

class ActivateLeaseSerializer(serializers.Serializer):
    selected_space = serializers.DecimalField(
        max_digits=20, decimal_places=2, min_value=Decimal("0.01")
    )
    term_months = serializers.IntegerField(min_value=1, max_value=36)
    start_date = serializers.DateField()

class ActivateLeaseResponseSerializer(serializers.Serializer):
    lease_id = serializers.UUIDField(source="id")
    status = serializers.CharField()
    selected_space = serializers.DecimalField(max_digits=20, decimal_places=2)
    term_months = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()