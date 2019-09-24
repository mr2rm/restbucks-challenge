from django.db.models import Sum, F
from rest_framework import serializers

from app.models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		exclude = ['created_at', 'last_modified', 'slug']


class OrderItemSerializer(serializers.ModelSerializer):
	options = serializers.SerializerMethodField()
	item_price = serializers.SerializerMethodField()
	product = ProductSerializer()

	class Meta:
		model = OrderItem
		fields = ['product', 'options', 'count', 'item_price']

	def get_options(self, order_item):
		options = {}
		for field in OrderItem.customization_options.keys():
			value = getattr(order_item, field, None)
			if value:
				options.update({field: value})
		return options

	def get_item_price(self, order_item):
		return order_item.count * order_item.product.price


class OrderSerializer(serializers.ModelSerializer):
	customer = serializers.StringRelatedField()
	total_price = serializers.SerializerMethodField()
	products = OrderItemSerializer(many=True, read_only=True, source='order_item_set')

	class Meta:
		model = Order
		exclude = ['last_modified']

	def get_total_price(self, order):
		return order.order_item_set.annotate(
			item_price=F('product__price') * F('count')
		).aggregate(
			total_price=Sum('item_price')
		).get('total_price')
