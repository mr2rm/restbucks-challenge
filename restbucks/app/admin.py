from django.contrib import admin

from app.models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'price', 'slug']
	search_fields = ['name', 'slug']
	readonly_fields = ['slug']


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 1
	raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'customer', 'delivery_method', 'delivery_address', 'status', 'is_active']
	list_editable = ['status', 'is_active']
	list_filter = ['is_active', 'status', 'delivery_method']
	search_fields = ['id', 'customer__username', 'delivery_address']
	raw_id_fields = ['customer']
	inlines = [OrderItemInline]
