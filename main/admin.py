from django.contrib import admin

from main.models import Printer, Cartridge, Structure, CartridgeStructure, CartridgeMovement, CartridgeOrder


class CartridgeStructureInline(admin.StackedInline):
    model = CartridgeStructure
    extra = 1


class CartridgeMovementInline(admin.StackedInline):
    model = CartridgeMovement
    extra = 1


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    inlines = (CartridgeStructureInline,)


@admin.register(Cartridge)
class CartridgeAdmin(admin.ModelAdmin):
    inlines = (CartridgeMovementInline, CartridgeStructureInline,)


@admin.register(CartridgeOrder)
class CartridgeOrderAdmin(admin.ModelAdmin):
    list_display = ('structure', 'cartridge', 'count')


admin.site.register(Printer)
