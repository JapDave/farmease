from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.tasks import mail_sender_newcustomer
from .models import Customer,Cart
import hashlib

@receiver(post_save, sender=Customer)
def notify_user(sender,instance,created,**kwargs):
  if created:
    cart_obj = Cart(user=instance)
    cart_obj.save()
    # mail_sender_newcustomer.delay(instance.email)
    instance.password = hashlib.sha256(str.encode(instance.password)).hexdigest()
    super(Customer, instance).save()



