from rest_framework import serializers

from app.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		exclude = ['created_at', 'last_modified', 'slug']


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'
