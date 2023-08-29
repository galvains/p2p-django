from django.db import models


class TicketsTable(models.Model):
    nick_name = models.CharField(max_length=50)
    price = models.FloatField()
    orders = models.CharField(max_length=7)
    available = models.FloatField()
    max_limit = models.FloatField()
    min_limit = models.FloatField()
    rate = models.CharField(max_length=8)
    pay_methods = models.TextField()
    currency = models.CharField(max_length=5)
    coin = models.CharField(max_length=5)
    trade_type = models.CharField(max_length=5)
    link = models.URLField()
    time_create = models.DateTimeField()
    exchange = models.ForeignKey('ExchangeTable', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.nick_name


class ExchangeTable(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name
