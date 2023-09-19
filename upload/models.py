from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Log(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='logs/')

@receiver(pre_save, sender=Log)
def set_name_from_file(sender, instance, **kwargs):
    if not instance.name and instance.file:
        file_name = instance.file.name
        instance.name = file_name.split('/')[-1]

