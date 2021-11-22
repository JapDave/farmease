from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import SubAdmin
from .tasks import mail_sender_newadmin
import  hashlib

@receiver(post_save, sender=SubAdmin)
def notify_user(sender, instance, created, **kwargs):
    if created:
       
        # mail_sender_newadmin.delay(instance.email,instance.password)

        instance.password = hashlib.sha256(str.encode(instance.password)).hexdigest()
        super(SubAdmin, instance).save()
