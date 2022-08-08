from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save


class Printer(models.Model):
    name = models.CharField(max_length=100)
    manufacture = models.CharField(max_length=100, choices=(('Kyocera', 'Kyocera'), ('HP', 'HP')))

    def __str__(self):
        return f'{self.manufacture} - {self.name}'


class Cartridge(models.Model):
    name = models.CharField(max_length=100)
    manufacture = models.CharField(max_length=100, choices=(('Kyocera', 'Kyocera'), ('HP', 'HP')))
    printer = models.ForeignKey(Printer, related_name='cartridges', on_delete=models.SET_NULL, blank=True, null=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.manufacture} - {self.name}'


class Structure(models.Model):
    name = models.CharField(max_length=100)
    printers = models.ManyToManyField(Printer, related_name='structures', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


# # Structure receivers
# @receiver(post_save, sender=Structure)
# def create_cartridges(sender, instance, **kwargs):
#     for printer in instance.printers.all():
#         for cartridge in printer.cartridges.all():


class CartridgeStructure(models.Model):
    cartridge = models.ForeignKey(Cartridge, related_name='cartridges', on_delete=models.CASCADE)
    structure = models.ForeignKey(Structure, related_name='cartridges', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.structure.name} {self.cartridge.name} {self.count}'


class CartridgeMovement(models.Model):
    count = models.PositiveIntegerField(default=1)
    cartridge = models.ForeignKey(Cartridge, related_name='movements', on_delete=models.CASCADE)
    from_structure = models.ForeignKey(Structure, related_name='from_movements', on_delete=models.CASCADE, blank=True,
                                       null=True)
    to_structure = models.ForeignKey(Structure, related_name='to_movements', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)

    def change_count_on_structures(self):
        if self.from_structure:
            for cs in self.from_structure.cartridges.all():
                if cs.cartridge == self.cartridge:
                    cs.count -= self.count
                    if cs.count < 0:
                        return True, f'{self.from_structure.name} нет картриджей на остатке'
                    cs.save()
        for cs in self.to_structure.cartridges.all():
            if cs.cartridge == self.cartridge:
                cs.count += self.count
                cs.save()
        return False, ''

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_error, text_error = self.change_count_on_structures()
        if not is_error:
            super().save(force_insert, force_update, using, update_fields)
        else:
            print(text_error)

    def __str__(self):
        return f'{self.cartridge.name}'


@receiver(pre_delete, sender=CartridgeMovement)
def create_cartridges(sender, instance, **kwargs):
    instance.from_structure, instance.to_structure = instance.to_structure, instance.from_structure
    instance.change_count_on_structures()


class CartridgeOrder(models.Model):
    structure = models.ForeignKey(Structure, related_name='orders', on_delete=models.CASCADE)
    cartridge = models.ForeignKey(Cartridge, related_name='orders', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    date_create = models.DateTimeField(auto_now_add=True)
    date_complete = models.DateTimeField()
    user_create = models.CharField(max_length=100, blank=True, null=True)
    user_complete = models.CharField(max_length=100, blank=True, null=True)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.cartridge.name} -> {self.structure.name}'
