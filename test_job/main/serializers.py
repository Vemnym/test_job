import shutil
import csv
import os
from rest_framework import serializers
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
    class Meta:
        model = CsvFiles
        fields = ("id", 'file')

    def create(self, validated_data):
        CsvFiles.objects.all().delete()
        Deals.objects.all().delete()
        Gems.objects.all().delete()
        Clients.objects.all().delete()

        try:
            shutil.rmtree('files')
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

        gems_list = list(set([x for x in gems_list if gems_list.count(x) == 1]))

        for item in gems_list:
            Gems.objects.filter(name=item).delete()

        return file
