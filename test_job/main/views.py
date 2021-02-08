from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

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


# @api_view(['GET'])
# def show_clients(request):
#     all_clients = Clients.objects.all().order_by('-spent_money')[:5]
#     serializer = ClientsSerializer(all_clients, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# def upload_file(request):
#     serializer = CsvFilesSerializer(data=request.data, files=request.FILES)
#
#     if serializer.is_valid():
#         serializer.save()
#
#     return Response(serializer.data)
