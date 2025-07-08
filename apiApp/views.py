from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apiApp.models import Product, Category, Cart, CartItem
from apiApp.serializers import *


# Create your views here.
@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)

@api_view(['Get'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)
@api_view(['Get'])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request, slug):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')
    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)
    cartitem, created = CartItem.objects.get(cart=cart, product=product)
    cartitem.quantity += 1
    cartitem.save()
    serializer = CartSerializer(cart)
    return Response(serializer.data)
