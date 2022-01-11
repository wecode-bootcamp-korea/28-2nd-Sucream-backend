from django.db import models

from products.models import ProductSize
from users.models    import User
from cores.models    import TimeStampModel

class Bidding(TimeStampModel):
    price          = models.DecimalField(max_digits=11, decimal_places=2)
    is_buyer       = models.BooleanField()
    user           = models.ForeignKey(User, on_delete=models.CASCADE)
    products_sizes = models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    class Meta:
        db_table = "biddings"

class Order(TimeStampModel):
    buyer          = models.ForeignKey(User, related_name='order_buy', on_delete=models.CASCADE)
    seller         = models.ForeignKey(User, related_name='order_sell', on_delete=models.CASCADE)
    price          = models.DecimalField(max_digits=11, decimal_places=2)
    products_sizes = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    status         = models.ForeignKey("Status", on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"

class Status(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "status"