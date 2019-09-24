from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from app.views import ListProduct, OrderViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
	url(r'^api/v1/products/', ListProduct.as_view(), name='products'),
	url(r'^api/v1/', include(router.urls, namespace='orders')),
]
