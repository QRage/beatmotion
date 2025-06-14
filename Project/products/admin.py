from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase

from .models import Category, Product, ProductAttributeValue, ProductAttribute, ProductImage


class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    autocomplete_fields = ['attribute']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ProductImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['preview']
    fields = ['image', 'preview']
    show_change_link = False
    
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return ""
    preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ProductAttributeValueInline, ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
