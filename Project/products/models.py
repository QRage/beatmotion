from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models import Max

from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    article = models.CharField(max_length=10, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
    'Category', on_delete=models.SET_NULL, null=True, blank=True,
    related_name='products', verbose_name=_("Category")
    )

    def save(self, *args, **kwargs):
        if not self.article:
            last_id = Product.objects.aggregate(Max('id'))['id__max'] or 0
            next_id = last_id + 1
            self.article = f"{next_id:05d}"
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
