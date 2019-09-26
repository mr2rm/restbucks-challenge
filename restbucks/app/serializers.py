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

	def to_representation(self, instance):
		options = super(OptionsSerializer, self).to_representation(instance)
		cleaned_options = filter(lambda option: option[1], options.items())
		return dict(cleaned_options)


class OrderItemSerializer(serializers.ModelSerializer):
	options = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()

	class Meta:
		model = OrderItem
		fields = ['product', 'count', 'options', 'price']

	@staticmethod
	def get_options(order_item):
		return OptionsSerializer(order_item).data

	@staticmethod
	def get_price(order_item):
		return order_item.price


class OrderSerializer(serializers.ModelSerializer):
	customer = serializers.StringRelatedField()
	total_price = serializers.SerializerMethodField()
	items = OrderItemSerializer(many=True, source='order_item_set')

	class Meta:
		model = Order
		exclude = ['is_active', 'last_modified']

	@staticmethod
	def get_total_price(order):
		return order.price


class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):
	options = OptionsSerializer(required=False)

	class Meta:
		model = OrderItem
		fields = ['product', 'count', 'options']


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
	items = OrderItemCreateUpdateSerializer(many=True)

	class Meta:
		model = Order
		fields = ['items', 'delivery_method', 'delivery_address']

	@staticmethod
	def create_order_items(order, data):
		for item in data:
			options = item.pop('options', {})
			OrderItem.objects.create(**item, **options, order=order)

	def validate(self, attrs):
		errors = {}

		if attrs.get('delivery_method') == Order.TAKE_AWAY and not attrs.get('delivery_address'):
			errors.update({'delivery_address': ['This field is required.']})

		has_error, items_errors = False, []
		for item in attrs['items']:
			product, item_errors = item['product'], {}
			options = item.setdefault('options', {})

			for key, products in OrderItem.customization_options.items():
				if options.get(key):
					if product.slug not in products:
						key_errors = item_errors.setdefault('options', {}).setdefault(key, [])
						key_errors.append("This option is not available for the product.")

				elif key in OrderItem.default_values and product.slug in products:
					options.update({key: OrderItem.default_values[key]})

			has_error |= bool(item_errors)
			items_errors.append(item_errors)

		if has_error:
			errors.update({'items': items_errors})

		if errors:
			raise ValidationError(errors)

		return attrs

	def create(self, validated_data):
		items = validated_data.pop('items')
		request = self.context['request']
		order = Order.objects.create(**validated_data, customer=request.user)
		self.create_order_items(order, items)
		return order

	def update(self, instance, validated_data):
		items = validated_data.pop('items')
		order = super(OrderCreateUpdateSerializer, self).update(instance, validated_data)
		order.items.clear()
		self.create_order_items(order, items)
		return order

	def to_representation(self, instance):
		return OrderSerializer(instance).data
