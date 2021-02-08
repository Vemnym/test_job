from django.conf.global_settings import MEDIA_URL
from django.db import models


# data from deals.csv
class Deals(models.Model):
    customer = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()


class CsvFiles(models.Model):
    deals = models.FileField(upload_to=MEDIA_URL, max_length=100, blank=True)

    def __str__(self):
        return self.name


class Gems(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Clients(models.Model):
    username = models.CharField(max_length=30)
    spent_money = models.IntegerField()
    gems = models.ManyToManyField(Gems)



