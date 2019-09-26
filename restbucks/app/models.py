from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum
from django.utils.text import slugify


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

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Product, self).save(*args, **kwargs)


class Order(AbstractTimeStamped):
	WAITING, PREPARATION, READY, DELIVERED = 'waiting', 'preparation', 'ready', 'delivered'
	TAKE_AWAY, IN_SHOP = 'take_away', 'in_shop'

	STATUS_CHOICES = [
		(WAITING, 'در انتظار'),
		(PREPARATION, 'در حال آماده سازی'),
		(READY, 'آماده شده'),
		(DELIVERED, 'تحویل داده شده'),
	]
	DELIVERY_METHOD_CHOICES = [
		(IN_SHOP, 'در فروشگاه'),
		(TAKE_AWAY, 'بیرون بر'),
	]

	customer = models.ForeignKey(User, verbose_name='مشتری')
	items = models.ManyToManyField(Product, through='OrderItem', verbose_name='اقلام')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=WAITING, verbose_name='وضعیت')
	delivery_method = models.CharField(
		max_length=20, null=True, blank=True, verbose_name='نحوه تحویل',
		choices=DELIVERY_METHOD_CHOICES, default=IN_SHOP
	)
	delivery_address = models.TextField(null=True, blank=True, verbose_name='آدرس تحویل')
	is_active = models.BooleanField(default=True, verbose_name='فعال')

	class Meta:
		verbose_name = 'سفارش'
		verbose_name_plural = 'سفارش‌ها'
		default_related_name = 'order_set'

	def __str__(self):
		return '%d (%s)' % (self.id, self.get_status_display())

	def clean(self):
		super(Order, self).clean()
		if self.delivery_method == self.TAKE_AWAY and not self.delivery_address:
			raise ValidationError({'delivery_address': ['This field is required.']})

	@property
	def price(self):
		return self.order_item_set.annotate(
			item_price=F('product__price') * F('count')
		).aggregate(
			total_price=Sum('item_price')
		).get('total_price')


class OrderItem(AbstractTimeStamped):
	SKIM, SEMI, WHOLE = 'skim', 'semi', 'whole'
	SMALL, MEDIUM, LARGE = 'small', 'medium', 'large'
	SINGLE, DOUBLE, TRIPLE = 'single', 'double', 'triple'
	CHOCOLATE_CHIP, GINGER = 'chocolate_chip', 'ginger'

	MILK_CHOICES = [
		(SKIM, 'کف - کم'),
		(SEMI, 'نصف - متوسط'),
		(WHOLE, 'کامل - زیاد'),
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
	count = models.PositiveIntegerField(default=1, verbose_name='تعداد')
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

	def __str__(self):
		return '%s (%d)' % (self.product.name, self.count)

	def clean(self):
		super(OrderItem, self).clean()
		for field, products in self.customization_options.items():
			if getattr(self, field, None):
				if self.product.slug not in products:
					raise ValidationError({field: ["This option is not available for the product."]})
			elif field in self.default_values and self.product.slug in products:
				setattr(self, field, self.default_values[field])

	@property
	def price(self):
		return self.count * self.product.price
