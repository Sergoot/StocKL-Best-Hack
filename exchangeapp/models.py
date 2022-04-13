from django.db import models

from users.models import CustomUser


class Stock(models.Model):
    name = models.CharField(max_length=4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,blank=True, default='')
    price = models.FloatField(default=1, null=True)


    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default='')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, default='')
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=3,verbose_name='стоимость', default=0, null=True)

