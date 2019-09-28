from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from app.models import Product, Order, OrderItem


class ProductModelTests(TestCase):
	def test_creation(self):
		product = Product.objects.create(name='Hot Chocolate', price=1000)

		# check if created_at, last_modified and slug are set
		for field in ['created_at', 'last_modified', 'slug']:
			self.assertIsNotNone(getattr(product, field, None))

		# check if slug is valid
		self.assertEqual(product.slug, 'hot-chocolate')

	def test_update(self):
		product = Product.objects.create(name='Hot Chocolate', price=1000)

		# update product
		product.name = 'Latte'
		product.save()

		# check if slug has been updated
		self.assertEqual(product.slug, 'latte')


class OrderModelTests(TestCase):
	fixtures = ['product.json']

	def setUp(self):
		self.user = User.objects.create_user('test')

	def test_creation(self):
		order = Order.objects.create(customer=self.user)
		for i in range(1, 4):
			OrderItem.objects.create(order=order, product_id=i)

		# check if items added
		self.assertEqual(order.items.count(), 3)

	def test_delivery_method(self):
		order = Order(customer=self.user, delivery_method=Order.TAKE_AWAY)

		# check if address is mandatory for take away order
		try:
			order.full_clean()
			self.fail('Oops')
		except ValidationError as e:
			self.assertIn('delivery_address', e.message_dict)

	def test_price(self):
		order, total_price = Order.objects.create(customer=self.user), 0
		for i in range(1, 4):
			order_item = OrderItem.objects.create(order=order, product_id=i, count=i)
			total_price += i * order_item.product.price

		# check if order price is correct
		self.assertEqual(order.price, total_price)


class OrderItemModelTests(TestCase):
	fixtures = ['product.json']

	def setUp(self):
		self.user = User.objects.create_user('test')

	def test_creation(self):
		pass

	def test_options(self):
		# check default
		# check validation
		pass

	def test_price(self):
		pass
