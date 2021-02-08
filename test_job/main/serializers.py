import re
import shutil
import csv
import os

from django.conf.global_settings import MEDIA_URL, MEDIA_ROOT
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CsvFiles, Clients, Gems, Deals


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
        fields = ['username', 'spent_money', 'gems']


class CsvFilesSerializer(serializers.ModelSerializer):
    deals = serializers.FileField(allow_empty_file=False, use_url=False)

    class Meta:
        model = CsvFiles
        fields = ["deals", ]

    def create(self, validated_data):
        CsvFiles.objects.all().delete()
        Deals.objects.all().delete()
        Gems.objects.all().delete()
        Clients.objects.all().delete()

        try:
            shutil.rmtree("main\media")
        except:
            pass

        pattern = r"csv$"
        if re.search(pattern, "{}".format(validated_data['deals'])):
            deals = self.Meta.model(**validated_data)
            deals.save()
        else:
            error = {'Status': 'Error',
                     'Desc': '<Неверный формат файла> - в процессе обработки файла произошла ошибка.'}
            raise serializers.ValidationError(error)

        workpath = "main\media"
        nameoffile = str(validated_data['deals']).replace(" — ", "__")

        try:
            f = open(os.path.join(workpath, "{}".format(nameoffile)), encoding='utf-8')
        except FileNotFoundError as e:
            error = {'Status': "Error",
                     "Desc": "<{}>- в процессе обработки файла произошла ошибка.".format(e.args)
                     if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)
        except Exception as e:
            error = {'Status': "Error",
                     "Desc": "<{}>- в процессе обработки файла произошла ошибка.".format(",".join(e.args))
                     if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)

        reader = csv.reader(f)
        next(reader)
        try:
            for row in reader:
                Deals(
                    customer=row[0],
                    item=row[1],
                    total=row[2],
                    quantity=row[3],
                    date=row[4]
                ).save()
        except Exception as e:
            error = {'Status': "Error",
                     "Desc": "<{}>- в процессе обработки файла произошла ошибка.".format(e.args)
                     if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)

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

        gems_list = list(set([x for x in gems_list if gems_list.count(x) == 1]))

        for item in gems_list:
            Gems.objects.filter(name=item).delete()

        return deals
