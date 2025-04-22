from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Module, TheoryContent

@receiver(post_save, sender=Module)
def create_module_content(sender, instance, created, **kwargs):
    if created and instance.module_type == 'theory':
        TheoryContent.objects.create(module=instance)