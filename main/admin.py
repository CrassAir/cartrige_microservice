from django.contrib import admin

from main.models import Printer, Cartridge, Structure, CartridgeMovement, CartridgeOrder, TypeCartridge


class CartridgeMovementInline(admin.TabularInline):
    model = CartridgeMovement
    readonly_fields = ('date_create',)
    extra = 1


class CartridgeMovementFromInline(admin.TabularInline):
    model = CartridgeMovement
    fk_name = 'to_structure'
    readonly_fields = ('date_create',)
    extra = 1


class CartridgeInline(admin.TabularInline):
    model = Cartridge
    extra = 1


class TypeCartridgeInline(admin.TabularInline):
    model = TypeCartridge
    extra = 1


@admin.register(TypeCartridge)
class TypeCartridge(admin.ModelAdmin):
    inlines = (CartridgeInline,)
    readonly_fields = ('all_count', 'empty_count', 'broken_count')
    list_display = ('__str__', 'all_count', 'empty_count', 'broken_count')


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    inlines = (CartridgeInline, CartridgeMovementFromInline)
    readonly_fields = ('all_count', 'empty_count', 'broken_count')
    list_display = ('__str__', 'all_count', 'empty_count', 'broken_count')


@admin.register(Cartridge)
class CartridgeAdmin(admin.ModelAdmin):
    inlines = (CartridgeMovementInline,)
    list_display = ('__str__', 'is_empty', 'is_broken', 'structure')


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    inlines = (TypeCartridgeInline,)


@admin.register(CartridgeOrder)
class CartridgeOrderAdmin(admin.ModelAdmin):
    list_display = ('structure', 'cartridge', 'count')
