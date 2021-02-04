from django.db import models


# data from deals.csv
class Deals(models.Model):
    customer = models.CharField(max_length=30)
    item = models.CharField(max_length=30)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()


class CsvFiles(models.Model):
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to='files', max_length=100, blank=True)
