"""from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Klient, Fryzjer


############# KLIENT ##############
@receiver(post_save, sender=User)
def create_client(sender, instance, created, **kwargs):
    if created:
        Klient.objects.create(user=instance, imie=instance.username)


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    instance.klient.save()
"""




