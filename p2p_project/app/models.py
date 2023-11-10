from django.db import models
from django.urls import reverse


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
    trade_type = models.BooleanField()
    link = models.URLField()
    time_create = models.DateTimeField()
    exchange = models.ForeignKey('ExchangeTable', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-price', '-time_create']
        verbose_name_plural = "Tickets table"

    def __str__(self):
        return self.nick_name

    def get_absolute_url(self):
        return reverse('ticket', kwargs={'post_id': self.pk})


class ExchangeTable(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name
