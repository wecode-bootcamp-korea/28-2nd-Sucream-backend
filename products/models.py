from django.db import models

from cores.models import TimeStampModel

class Product(TimeStampModel):
    name          = models.CharField(max_length=100)
    korean_name   = models.CharField(max_length=100)
    model_number  = models.CharField(max_length=20)
    color         = models.CharField(max_length=100)
    release_at    = models.DateField()
    retail_price  = models.DecimalField(max_digits=11, decimal_places=2)
    thumbnail_url = models.CharField(max_length=500)
    brand         = models.ForeignKey("Brand", on_delete=models.CASCADE)
    sizes         = models.ManyToManyField("Size", related_name="product", through='ProductSize')
    users         = models.ManyToManyField("users.User", related_name="product", through="users.Like")

    class Meta:
        db_table = "products"

class Brand(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "brands"

class Size(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "sizes"

class ProductSize(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size    = models.ForeignKey("Size", on_delete=models.CASCADE)

    class Meta:
        db_table = "products_sizes"

class Image(models.Model):
    url     = models.CharField(max_length=500)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"