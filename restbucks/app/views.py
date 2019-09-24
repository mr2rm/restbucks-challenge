from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.models import Product, Order
from app.serializers import ProductSerializer, OrderSerializer


class ListProduct(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class OrderViewSet(ModelViewSet):
	serializer_class = OrderSerializer
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = Order.objects.all()

	def get_queryset(self):
		if not self.request.user.is_staff:
			return Order.objects.filter(customer=self.request.user)
		return super(OrderViewSet, self).get_queryset()
