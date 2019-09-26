from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from app.models import Product, Order
from app.serializers import ProductSerializer, OrderSerializer, OrderCreateUpdateSerializer


class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()


class OrderViewSet(ModelViewSet):
	serializer_class = OrderSerializer
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = Order.objects.all()

	def get_queryset(self):
		if not self.request.user.is_staff:
			return Order.objects.filter(customer=self.request.user)
		return super(OrderViewSet, self).get_queryset()

	def get_object(self):
		order = super(OrderViewSet, self).get_object()
		if order.status != Order.WAITING and self.action in ['update', 'delete']:
			raise Http404
		return order

	def get_serializer_class(self):
		if self.action in ['create', 'update']:
			return OrderCreateUpdateSerializer
		return super(OrderViewSet, self).get_serializer_class()
