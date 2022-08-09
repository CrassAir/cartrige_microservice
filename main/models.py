from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save, m2m_changed


class Printer(models.Model):
    name = models.CharField(max_length=100)
    manufacture = models.CharField(max_length=100, choices=(('Kyocera', 'Kyocera'), ('HP', 'HP')))

    def __str__(self):
        return f'{self.manufacture} - {self.name}'


class TypeCartridge(models.Model):
    name = models.CharField(max_length=100)
    manufacture = models.CharField(max_length=100, choices=(('Kyocera', 'Kyocera'), ('HP', 'HP')))
    printer = models.ForeignKey(Printer, related_name='cartridges', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def all_count(self):
        return len(self.cartridges.all())

    @property
    def empty_count(self):
        return len(self.cartridges.filter(is_empty=True))

    @property
    def broken_count(self):
        return len(self.cartridges.filter(is_broken=True))

    def __str__(self):
        return f'{self.manufacture} - {self.name}'


class Structure(models.Model):
    name = models.CharField(max_length=100)
    printers = models.ManyToManyField(Printer, related_name='structures', blank=True, null=True)
    is_store = models.BooleanField(default=False)
    is_refueling = models.BooleanField(default=False)

    @property
    def all_count(self):
        return len(self.cartridges.all())

    @property
    def empty_count(self):
        return len(self.cartridges.filter(is_empty=True))

    @property
    def broken_count(self):
        return len(self.cartridges.filter(is_broken=True))

    def __str__(self):
        return f'{self.name}'


class Cartridge(models.Model):
    id = models.AutoField(primary_key=True, unique=True, default=100000)
    type = models.ForeignKey(TypeCartridge, related_name='cartridges', on_delete=models.CASCADE)
    is_empty = models.BooleanField(default=False)
    is_broken = models.BooleanField(default=False)
    structure = models.ForeignKey(Structure, related_name='cartridges', on_delete=models.SET_NULL, null=True,
                                  blank=True)

    def __str__(self):
        return f'{self.id} {self.type.name}'


class CartridgeOrder(models.Model):
    structure = models.ForeignKey(Structure, related_name='orders', on_delete=models.CASCADE)
    type_cartridge = models.ForeignKey(TypeCartridge, related_name='orders', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    date_complete = models.DateTimeField(blank=True, null=True)
    user_create = models.CharField(max_length=100, blank=True, null=True)
    user_complete = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.type_cartridge} -> {self.structure.name}'


class CartridgeMovement(models.Model):
    cartridge = models.ForeignKey(Cartridge, related_name='movements', on_delete=models.CASCADE)
    from_structure = models.ForeignKey(Structure, related_name='from_movements', on_delete=models.CASCADE, blank=True,
                                       null=True)
    to_structure = models.ForeignKey(Structure, related_name='to_movements', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    user_fulfilled = models.CharField(max_length=100, blank=True, null=True)
    date_confirmed = models.DateTimeField(blank=True, null=True)
    user_confirmed = models.CharField(max_length=100, blank=True, null=True)
    order = models.ForeignKey(CartridgeOrder, related_name='movements', on_delete=models.SET_NULL, blank=True,
                              null=True)

    def __str__(self):
        return f'{self.pk}'


@receiver(post_save, sender=CartridgeMovement)
def create_cartridges(sender, instance, **kwargs):
    instance.cartridge.structure = instance.to_structure
    instance.cartridge.save()


@receiver(pre_delete, sender=CartridgeMovement)
def delete_cartridges(sender, instance, **kwargs):
    instance.cartridge.structure = instance.from_structure
    instance.cartridge.save()
