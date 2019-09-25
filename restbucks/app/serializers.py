from django.db.models import Sum, F
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		exclude = ['created_at', 'last_modified', 'slug']


class OptionsSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = ['milk', 'size', 'shots', 'kind']


class OrderItemSerializer(serializers.ModelSerializer):
	options = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()

	class Meta:
		model = OrderItem
		fields = ['product', 'count', 'price', 'options']

	def get_options(self, order_item):
		options_data = OptionsSerializer(instance=order_item).data
		result = {}
		for field, value in options_data.items():
			if value:
				result.update({field: value})
		return result

	def get_price(self, order_item):
		return order_item.count * order_item.product.price


class OrderSerializer(serializers.ModelSerializer):
	customer = serializers.StringRelatedField()
	total_price = serializers.SerializerMethodField()
	products = OrderItemSerializer(many=True, source='order_item_set')

	class Meta:
		model = Order
		exclude = ['last_modified']

	def get_total_price(self, order):
		return order.order_item_set.annotate(
			item_price=F('product__price') * F('count')
		).aggregate(
			total_price=Sum('item_price')
		).get('total_price')


class OrderItemCreateSerializer(serializers.ModelSerializer):
	options = OptionsSerializer(required=False)

	class Meta:
		model = OrderItem
		fields = ['product', 'count', 'options']


class OrderCreateSerializer(serializers.ModelSerializer):
	products = OrderItemCreateSerializer(many=True)

	class Meta:
		model = Order
		fields = ['products', 'delivery_method', 'delivery_address']

	def to_representation(self, instance):
		return OrderSerializer(instance=instance).data

	def validate(self, attrs):
		if attrs.get('delivery_method') == Order.TAKE_AWAY and not attrs.get('delivery_address'):
			raise ValidationError({'delivery_address': ['This field is required.']})

		for order_item in attrs.get('products'):
			for key in order_item.get('options', {}):
				product_slug = order_item.get('product').slug
				if product_slug not in OrderItem.customization_options.get(key, []):
					raise ValidationError({'options': ["'%s' option is not valid for '%s'" % (key, product_slug)]})

		# TODO: set default values

	def create(self, validated_data):
		products_data = validated_data.pop('products')
		customer = self.context['request'].user
		order = Order.objects.create(**validated_data, customer=customer)
		for product_data in products_data:
			options = product_data.pop('options', {})
			OrderItem.objects.create(**product_data, **options, order=order)
		return order
