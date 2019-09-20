from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from app.functions import convert_to_text


class AbstractTimeStamped(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
	last_modified = models.DateTimeField(auto_now=True, verbose_name='آخرین به روزرسانی')

	class Meta:
		abstract = True


class Product(AbstractTimeStamped):
	name = models.CharField(max_length=20, verbose_name='نام')
	slug = models.SlugField(unique=True, verbose_name='شناسه یکتا')
	price = models.PositiveIntegerField(verbose_name='قیمت')

	class Meta:
		verbose_name = 'محصول'
		verbose_name_plural = 'محصولات'
		default_related_name = 'product_set'

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super(Product, self).save(*args, **kwargs)


class Order(AbstractTimeStamped):
	WAITING, PREPARATION, READY, DELIVERED = 'waiting', 'preparation', 'ready', 'delivered'
	TAKE_AWAY, IN_SHOP = 'take_away', 'in_shop'

	STATUS_CHOICES = [
		(WAITING, 'در انتظار'),
		(PREPARATION, 'در حال آماده سازی'),
		(READY, 'آماده'),
		(DELIVERED, 'تحویل داده شده'),
	]
	CONSUME_LOCATION_CHOICES = [
		(TAKE_AWAY, 'بیرون بر'),
		(IN_SHOP, 'در فروشگاه'),
	]

	customer = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, verbose_name='مشتری')
	products = models.ManyToManyField(Product, through='OrderItem', verbose_name='محصولات')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WAITING, verbose_name='وضعیت')
	consume_location = models.CharField(
		max_length=20, null=True, blank=True,
		choices=CONSUME_LOCATION_CHOICES, default=IN_SHOP
	)
	address = models.TextField(null=True, blank=True, verbose_name='آدرس')

	class Meta:
		verbose_name = 'سفارش'
		verbose_name_plural = 'سفارش‌ها'
		default_related_name = 'order_set'


class OrderItem(AbstractTimeStamped):
	SKIM, SEMI, WHOLE = 'skim', 'semi', 'whole'
	SMALL, MEDIUM, LARGE = 'small', 'medium', 'large'
	SINGLE, DOUBLE, TRIPLE = 'single', 'double', 'triple'
	CHOCOLATE_CHIP, GINGER = 'chocolate_chip', 'ginger'

	MILK_CHOICES = [
		(SKIM, 'کف (کم)'),
		(SEMI, 'نصف (متوسط)'),
		(WHOLE, 'کامل (زیاد)'),
	]
	SIZE_CHOICES = [
		(SMALL, 'کوچک'),
		(MEDIUM, 'متوسط'),
		(LARGE, 'بزرگ'),
	]
	SHOTS_CHOICES = [
		(SINGLE, 'تک شات'),
		(DOUBLE, 'دو شات'),
		(TRIPLE, 'سه شات'),
	]
	KIND_CHOICES = [
		(CHOCOLATE_CHIP, 'شکلاتی'),
		(GINGER, 'زنجبیلی'),
	]

	default_values = {
		'size': SMALL,
		'shots': SINGLE,
	}
	customization_options = {
		'milk': ['latte'],
		'size': ['cappuccino', 'hot-chocolate'],
		'shots': ['espresso'],
		'kind': ['cookie'],
	}

	order = models.ForeignKey(Order, verbose_name='سفارش')
	product = models.ForeignKey(Product, verbose_name='محصول')
	count = models.PositiveIntegerField(verbose_name='تعداد')
	milk = models.CharField(
		max_length=20, null=True, blank=True, choices=MILK_CHOICES,
		verbose_name='شیر', help_text='Latte'
	)
	size = models.CharField(
		max_length=20, null=True, blank=True, choices=SIZE_CHOICES,
		verbose_name='اندازه', help_text='Cappuccino and Hot Chocolate'
	)
	shots = models.CharField(
		max_length=20, null=True, blank=True, choices=SHOTS_CHOICES,
		verbose_name='شات', help_text='Espresso'
	)
	kind = models.CharField(
		max_length=20, null=True, blank=True, choices=KIND_CHOICES,
		verbose_name='نوع', help_text='Cookie'
	)

	class Meta:
		verbose_name = 'مورد سفارش'
		verbose_name_plural = 'اقلام سفارش'
		default_related_name = 'order_item_set'

	def clean(self):
		super(OrderItem, self).clean()
		for field, products in self.customization_options:
			if getattr(self, field, None):
				if self.product.slug not in products:
					raise ValidationError("'%s' option is only valid for %s" % (field, convert_to_text(products)))
			elif field in self.default_values:
				setattr(self, field, self.default_values[field])
