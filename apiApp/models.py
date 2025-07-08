from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    email =  models.EmailField(unique=True)
    profile_pic_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images', blank=True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.slug:
            unique_slug_generator = self.slug
            count = 1
            if Product.objects.filter(slug=self.slug).exists():
                unique_slug_generator = f"{unique_slug_generator}-{count}"
                count += 1
            self.slug = unique_slug_generator
        super().save(*args, **kwargs)

class Cart(models.Model):
    cart_code= models.CharField(max_length=11, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cart_code
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item')
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.cart_code}"