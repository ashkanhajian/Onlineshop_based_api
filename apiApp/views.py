from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apiApp.models import Product
from apiApp.serializers import ProductSerializer


# Create your views here.
@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)