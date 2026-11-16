from rest_framework import serializers


class BooksSerializer(serializers.Serializer):
    id = serializers.CharField()
    lease_id = serializers.CharField()
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)
    description = serializers.CharField()
    format_type = serializers.CharField(max_length=50)
    length = serializers.DecimalField(max_digits=6, decimal_places=2)
    width = serializers.DecimalField(max_digits=6, decimal_places=2)
    thickness = serializers.DecimalField(max_digits=6, decimal_places=2)
    unit_weight = serializers.DecimalField(max_digits=8, decimal_places=3)
    quantity = serializers.IntegerField()
    unit_volume = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_volume = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_weight = serializers.DecimalField(max_digits=14, decimal_places=3)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class InventoryPayloadSerializer(serializers.Serializer):
    lease_id = serializers.CharField()
    books = BooksSerializer()
    tag = serializers.CharField()
