from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "price",
        "is_available",
    ]
    list_filter = [
        "is_available",
    ]
    list_editable = [
        "price",
        "is_available",
    ]
