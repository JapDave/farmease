from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import Farmer,Token
from .tasks import mail_sender_newfarmer
import hashlib


@receiver(post_save, sender=Farmer)
def notify_user(sender, instance, created, **kwargs):
    if created:
        mail_sender_newfarmer.delay(instance.email)

        instance.password = hashlib.sha256(str.encode(instance.password)).hexdigest()
        super(Farmer, instance).save()

