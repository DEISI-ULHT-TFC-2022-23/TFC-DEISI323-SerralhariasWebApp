from django import template
from django.core import serializers

register = template.Library()

@register.filter
def get_first_image(product):
    first_image = product.images.first()

    if first_image is not None:
        return first_image.image.url
    
    return "/static/assets/imgs/highlight_default.png"

@register.filter
def get_images(product):
    return list(product.images.all())


@register.filter
def get_price(product):
    return "TBD" if product.price is None else f"{product.price:.2f} €"

@register.filter
def get_favorite_class(product, user_id):
    # Check if product is part of user wishlist
    if product.wish_set.filter(user_id=user_id).exists():
        return "filled"
    return ""


@register.filter
def get_image(category):
    if category.image:
        return category.image.url
    
    return "/static/assets/imgs/highlight_default.png"

@register.filter
def get_reference_number(order):
    return f"#{order.id:08d}"