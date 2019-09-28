from django.test import TestCase
from django.utils import timezone

from app.models import Product


class ProductModelTests(TestCase):
	def test_product_creation(self):
		product = Product.objects.create(name='Hot Chocolate', price=1000)

		# check if created_at, last_modified and slug are set
		self.assertIsNotNone(product.created_at)
		self.assertIsNotNone(product.last_modified)
		self.assertIsNotNone(product.slug)

		# check if created_at and last_modified are valid
		now = timezone.now()
		self.assertLess(product.created_at, now)
		self.assertLess(product.last_modified, now)

		# check if slug is valid
		self.assertEqual(product.slug, 'hot-chocolate')

	def test_product_update(self):
		product = Product.objects.create(name='Hot Chocolate', price=1000)

		# update product
		product.name = 'Latte'
		product.save()

		# check if slug has been updated
		self.assertEqual(product.slug, 'latte')

		# TODO: needs completion
		now = timezone.now()
		last_modified_diff = (now - product.last_modified).seconds
		self.assertLess(last_modified_diff, 1)
		created_at_diff = (now - product.created_at).seconds
