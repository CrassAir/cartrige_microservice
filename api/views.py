from rest_framework import viewsets

from api.serializers import PrinterSerializer, CartridgeSerializer, StructureSerializer
from main.models import Printer, Cartridge, Structure


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CartridgeViewSet(viewsets.ModelViewSet):
    queryset = Cartridge.objects.all()
    serializer_class = CartridgeSerializer


class StructureViewSet(viewsets.ModelViewSet):
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer


