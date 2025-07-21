

from django.shortcuts import render
from django.db.models import  Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apiApp.models import Product, Category, Cart, CartItem, Whislist
from apiApp.serializers import *
from django.contrib.auth import get_user_model
User = get_user_model()


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
def add_to_cart(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')
    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)
    cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cartitem.quantity += 1
    cartitem.save()
    serializer = CartSerializer(cartitem.cart)
    return Response(serializer.data)
@api_view(['PUT'])
def update_cart_quantity(request):
    cartitem_id = request.data.get('item_id')
    quantity = request.data.get("quantity")
    quantity = int(quantity)
    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()
    serializer = CartSerializer(cartitem.cart)
    return Response({'data': serializer.data, 'message': "CartItem updated"})

@api_view(['POST'])
def add_review(request):
    product_id = request.data.get('product_id')
    rating = request.data.get('rating')
    review = request.data.get('review')
    product = Product.objects.get(id=product_id)
    user = User.objects.get(email=request.data.get('email'))
    if Review.objects.filter(product=product, user=user).exists():
        return Response({'message': "You already drop a review."})
    review = Review.objects.create(product=product, user=user, rating=rating, review=review)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

@api_view(['PUT'])
def update_review(request,pk):
    review = Review.objects.get(id = pk)
    review_text = request.data.get('review')
    rating = request.data.get('rating')
    review.rating = rating
    review.review = review_text
    review.save()
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_review(request, pk):
    review= Review.objects.get(id=pk)
    review.delete()
    return Response({'message': "Review deleted"})


@api_view(['DELETE'])
def delete_cartitem(request, pk):
    cartitem= CartItem.objects.get(id=pk)
    cartitem.delete()
    return Response({'message': "CartItem deleted"})


@api_view(['POST'])
def add_to_whishlist(request):
    email = request.data.get('email')
    product_id = request.data.get('product_id')
    user = User.objects.get(email=email)
    product = Product.objects.get(id=product_id)

    whislist = Whislist.objects.filter(user=user, product=product)
    if whislist:
        whislist.delete()
        return Response({'message': "Whislist deleted"},status=204)

    new_wishlist = Whislist.objects.create(user=user, product=product)
    serializer = WishlistSerializer(new_wishlist)
    return Response(serializer.data)

@api_view(['GET'])
def product_search(request):
    query = request.query_params.get('query')
    if not query:
        return Response({'message': "You need to enter a query."})
    products = Product.objects.filter(Q(name__icontains=query)|
                                      Q(description__icontains=query)|
                                      Q(category__name__icontains=query)|
                                      Q(price__icontains=query))
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

