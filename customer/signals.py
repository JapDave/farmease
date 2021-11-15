from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Customer,Cart


@receiver(post_save, sender=Customer)
def notify_user(sender,instance,created,**kwargs):
   if created:
     cart_obj = Cart(user=instance)
     cart_obj.save()
