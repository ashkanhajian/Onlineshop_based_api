from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import  receiver
from apiApp.models import *


@receiver(post_save, sender=Review)
def update_rating(sender, instance, **kwargs):
    product = instance.product
    review = product.reviews.all()
    total_reviews = review.count()
    review_average = review.aggregate(Avg('rating'))['rating__avg'] or 0.0
    product_rating = ProductRating.objects.get_or_create(product=product)
    product_rating.average_rating = review_average
    product_rating.total = total_reviews

    product.save()
