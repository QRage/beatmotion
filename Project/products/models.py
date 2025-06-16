from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models import Max
from django.db import models


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


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    article = models.CharField(max_length=10, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='products', verbose_name=_("Category")
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.article:
            last_id = Product.objects.aggregate(Max('id'))['id__max'] or 0
            next_id = last_id + 1
            self.article = f"{next_id:05d}"
        super().save(*args, **kwargs)

    def get_attributes(self):
        return self.attributes.select_related('attribute').all()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ProductAttribute(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Attribute Name"))

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('product', 'attribute')
        verbose_name = _("Product Attribute Value")
        verbose_name_plural = _("Product Attribute Values")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
