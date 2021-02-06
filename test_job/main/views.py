import csv
import os

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Deals, CsvFiles, Clients, Gems
from rest_framework import serializers, viewsets
import shutil


# Create your views here.


# Serializers define the API representation.
# class DealsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Deals
#         fields = ["id", 'customer', 'item', 'total', 'quantity', 'date']


# ViewSets define the view behavior.
# class DealsViewSet(viewsets.ModelViewSet):
#     queryset = Deals.objects.all()
#     serializer_class = DealsSerializer

class GemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gems
        fields = ['name']


class ClientsSerializer(serializers.ModelSerializer):
    gems = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Clients
        fields = ["id", 'username', 'spent_money', 'gems']


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all().order_by('-spent_money')[:5]
    serializer_class = ClientsSerializer


class GemsViewSet(viewsets.ModelViewSet):
    queryset = Gems.objects.all()
    serializer_class = GemsSerializer


class CsvFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFiles
        fields = ("id", 'file')

    def create(self, validated_data):
        CsvFiles.objects.all().delete()
        Deals.objects.all().delete()
        Gems.objects.all().delete()
        Clients.objects.all().delete()


        dir_path = 'files'
        try:
            shutil.rmtree(dir_path)
        except:
            pass

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

        customers = Deals.objects.all().values("customer")

        clients = []
        for customer in customers:
            clients.append(customer["customer"])

        for client in set(clients):
            gems = []
            total_sum = 0
            client_query = list(Deals.objects.filter(customer=client))
            for query in client_query:
                total_sum += query.total
                gems.append(query.item)

            client_model = Clients(username=client,
                                   spent_money=total_sum)
            client_model.save()
            for gem in set(gems):
                gem_model = Gems(name=gem)
                gem_model.save()
                client_model.gems.add(gem_model)

        gems_correct = list(Clients.objects.all().order_by('-spent_money')[:5])
        gems_list = []

        for line in gems_correct:
            for gems in list(line.gems.all().values("name")):
                gems_list.append(gems['name'])
        print(gems_list)

        gems_list = list(set([x for x in gems_list if gems_list.count(x) == 1]))
        print(gems_list)

        # for line in gems_correct:
        #     for gems in list(line.gems.all().values("name")):
        for item in gems_list:
            Gems.objects.filter(name=item).delete()


            # print(Gems.objects.get(client=Clients.objects.get(username=client)).client.username)

        return file


class CsvFilesViewSet(viewsets.ModelViewSet):
    queryset = CsvFiles.objects.all()
    serializer_class = CsvFilesSerializer
