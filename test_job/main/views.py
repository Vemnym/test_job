import csv
import os

from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import Deals, CsvFiles
from rest_framework import serializers, viewsets
import shutil


# Create your views here.


# Serializers define the API representation.
class DealsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deals
        fields = ["id", 'customer', 'item', 'total', 'quantity', 'date']


# ViewSets define the view behavior.
class DealsViewSet(viewsets.ModelViewSet):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer


class CsvFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFiles
        fields = ('title', 'file')

    def create(self, validated_data):
        CsvFiles.objects.all().delete()
        Deals.objects.all().delete()
        dir_path = 'files'
        shutil.rmtree(dir_path)

        file = self.Meta.model(**validated_data)
        file.save()

        workpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        f = open(os.path.join(workpath, "files/{}".format(validated_data['file'])), encoding='utf-8')
        reader = csv.reader(f)
        for row in reader:
            _, created = Deals.objects.get_or_create(
                customer=row[0],
                item=row[1],
                total=row[2],
                quantity=row[3],
                date=row[4]
            )
        f.close()
        print(reader)
        print("nonononononononono")
        return file


class CsvFilesViewSet(viewsets.ModelViewSet):
    queryset = CsvFiles.objects.all()
    serializer_class = CsvFilesSerializer
