from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "title",
        "category",
        "price",
        "is_available",
    )

    list_display_links = ("title",)

    search_fields = (
        "title",
        "description",
    )

    list_filter = (
        "category",
        "is_available",
    )

    list_editable = (
        "price",
        "is_available",
    )

    ordering = ("title",)

    readonly_fields = ("image_preview",)

    fields = (
        "image_preview",
        "title",
        "category",
        "description",
        "price",
        "image",
        "is_available",
    )

    @admin.display(description="تصویر")
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="60" height="60" style="object-fit: cover; border-radius: 8px;">'

        return "بدون تصویر"