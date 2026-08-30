from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("title",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
    "title",
    "category",
    "price",
    "is_available",
    "created_at",
    )

    list_filter = (
        "category",
        "is_available",
    )

    search_fields = (
        "title",
        "description",
    )

    list_editable = (
        "price",
        "is_available",
    )

    autocomplete_fields = (
        "category",
    )

    ordering = (
        "category",
        "title",
    )
