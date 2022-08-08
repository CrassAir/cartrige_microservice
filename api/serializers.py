from rest_framework import serializers

from main.models import Cartridge, Printer, Structure, CartridgeMovement, CartridgeOrder


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'


class CartridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartridge
        fields = '__all__'
        depth = 1


class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Structure
        fields = '__all__'
        depth = 1


class CartridgeMovementSerializer(serializers.ModelSerializer):
    class Mate:
        model = CartridgeMovement
        fields = '__all__'
        depth = 1


class CartridgeOrderSerializer(serializers.ModelSerializer):
    class Mate:
        model = CartridgeOrder
        fields = '__all__'
        depth = 1
