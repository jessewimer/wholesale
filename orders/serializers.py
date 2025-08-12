from rest_framework import serializers
from .models import Order, OrderIncludes
from products.models import Product

class OrderIncludesSerializer(serializers.ModelSerializer):
    item_number = serializers.CharField(source='product.item_number', read_only=True)

    class Meta:
        model = OrderIncludes
        fields = ['item_number', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    includes = OrderIncludesSerializer(source='orderincludes_set', many=True)

    class Meta:
        model = Order
        fields = ['order_number', 'includes']

