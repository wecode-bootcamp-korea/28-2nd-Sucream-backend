from django.db import models

from cores.models    import TimeStampModel
from products.models import Product

class User(TimeStampModel):
    kakao_id = models.PositiveIntegerField(unique=True)
    email    = models.CharField(max_length=50)
    point    = models.DecimalField(max_digits=11, decimal_places=2, default=5000000)

    class Meta:
        db_table = "users"

class Like(models.Model):
    is_like = models.BooleanField(default=False)
    user    = models.ForeignKey("users.User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'