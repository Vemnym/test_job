from django.shortcuts import render
from .models import Deals
from rest_framework import routers, serializers, viewsets


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
