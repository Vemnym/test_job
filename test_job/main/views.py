from .models import CsvFiles, Clients, Gems
from rest_framework import viewsets, status
from .serializers import ClientsSerializer, GemsSerializer, CsvFilesSerializer


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all().order_by('-spent_money')[:5]
    serializer_class = ClientsSerializer
    http_method_names = ['get']


class GemsViewSet(viewsets.ModelViewSet):
    queryset = Gems.objects.all()
    serializer_class = GemsSerializer


class CsvFilesViewSet(viewsets.ModelViewSet):
    queryset = CsvFiles.objects.all()
    serializer_class = CsvFilesSerializer
