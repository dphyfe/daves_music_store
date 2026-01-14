"""
Serializers for the store API.
"""

from rest_framework import serializers

from .models import Category, Instrument, CartItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class InstrumentSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Instrument
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "brand",
            "condition",
            "price",
            "rating",
            "description",
            "specifications",
            "image",
            "in_stock",
            "featured",
            "created_at",
            "updated_at",
        ]

    def get_image(self, obj):
        url = obj.image_display_url
        request = self.context.get("request")
        if request and url:
            return request.build_absolute_uri(url)
        return url


class CartItemSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "instrument", "quantity", "subtotal", "added_at"]

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    item_count = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "session_key",
            "items",
            "item_count",
            "total",
            "created_at",
            "updated_at",
        ]

    def get_item_count(self, obj):
        return obj.get_item_count()

    def get_total(self, obj):
        return obj.get_total()
