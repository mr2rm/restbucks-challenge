from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from app.models import Product, Order
from app.serializers import ProductSerializer, OrderSerializer


class ListProduct(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
	serializer_class = OrderSerializer

	def get_queryset(self):
		return Order.objects.filter(customer=self.request.user)
