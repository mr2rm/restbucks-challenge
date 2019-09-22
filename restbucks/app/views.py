from rest_framework.generics import ListAPIView

from app.models import Product
from app.serializers import ProductSerializer


class ListProduct(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
