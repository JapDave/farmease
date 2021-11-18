from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Order


@shared_task(name='mail_sender_newcustomer')
def mail_sender_newcustomer(email):
     
   subject = 'New Account Registered'
   message = f''' Thank-you for registering into our site.'''

   email_from = settings.EMAIL_HOST_USER
   recepient  = [email,]
   send_mail(subject, message, email_from, recepient)
              


@shared_task(name='mail_sender_farmer')
def mail_sender_farmer(order_obj_id):
     
   order_obj = Order.objects.get(_id=order_obj_id)
   item_list = []
   # order_pair = {}
   for item in order_obj.items:
      order_pair = {
         'product': item.product,
         'qty': str(item.qty) +'kg'
      }
      item_list.append(order_pair)


   subject = 'Order Recieved'
   message = f''' An Order for an product for your enterprise is been recieved please check for status.
   Order Details are as follow- 
      Items - {item_list}
   
   Customer Details are as follow-
   Name - {order_obj.customer.name}
   contact - {order_obj.customer.contact}
   Address - {order_obj.address}

   For any inquiry feel free to contact.
   Thank you
   '''
   email_from = settings.EMAIL_HOST_USER
   recepient  = [order_obj.farmer.email,]

   send_mail(subject, message, email_from, recepient)



@shared_task(name='mail_sender_user')
def mail_sender_user(email):
      subject = 'Order Placed'
      message = f''' Thank-you for placing order,your package will be delievered soon. Check Out Details in Order History.
      For any inquiry feel free to contact.
      Thank you
      Keep Shopping 
      '''

      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

    