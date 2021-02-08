from django.conf.global_settings import MEDIA_URL
from django.db import models


class Deals(models.Model):
    customer = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()


class CsvFiles(models.Model):
    deals = models.FileField(upload_to=MEDIA_URL, max_length=100, blank=True)


class Gems(models.Model):
    name = models.CharField(max_length=30)


class Clients(models.Model):
    username = models.CharField(max_length=30)
    spent_money = models.IntegerField()
    gems = models.ManyToManyField(Gems)



