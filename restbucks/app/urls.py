from django.conf.urls import url, include

from app.views import ListProduct

urlpatterns = [
	url(r'^api/v1/products/$', ListProduct.as_view(), name='products'),
]
