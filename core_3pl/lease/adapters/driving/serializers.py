from rest_framework import serializers
from lease.models import Lease as LeaseModel

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