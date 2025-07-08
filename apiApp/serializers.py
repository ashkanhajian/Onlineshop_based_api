from rest_framework import serializers
from apiApp.models import Product, Category, CartItem, Cart


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','price']
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','slug','price','description']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']
class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id','name','image']

class CartItemListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','sub_total']

    def get_sub_total(self, cartitem):
        total = cartitem.product.price * cartitem.quantity
        return total

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemListSerializer(many=True, read_only=True)
    cart_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_items','cart_code']
    def get_cart_items(self, cart):
        items = cart.cart_items.all()
        total = sum([items.quantity * items.price for items in items])
        return total

class CartStatusSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','cart_code', 'total_quantity']
    def get_total_quantity(self, cart):
        items = cart.cart_items.all()
        total = sum([items.quantity * items.price for items in items])
        return total
