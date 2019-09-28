from django.test import TestCase
from django.utils import timezone

from app.models import Product


class ProductModelTests(TestCase):
	def test_product_creation(self):
		product = Product.objects.create(name='Hot Chocolate', price=100)

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
