from django.conf.urls import url, include
from rest_framework import routers

from app.views import OrderViewSet, ProductViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'products', ProductViewSet, basename='products')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
	url(r'^api/v1/', include(router.urls, namespace='orders')),
]
