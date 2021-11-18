from customer.models import Order
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task(name='mail_sender_newfarmer')
def mail_sender_newfarmer(email):
     
   subject = 'New Account Registered'
   message = f''' Thank-you for registering into our site.'''
   email_from = settings.EMAIL_HOST_USER
   recepient  = [email,]
   send_mail(subject, message, email_from, recepient)
              
    

@shared_task(name='mail_user_updatedorder')
def mail_user_updateorder(status,email,id):
   order_obj = Order.objects.get(_id=id)
  
   if status == '1':
      subject = 'Product Order Approved'
      message = f''' Your Order is approved and soon will be dispatched.'''
      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

   elif status == '2':
      subject = 'Product Order Dispatched'
      message = f''' Your Order is Dispatched and soon will be delivered.'''
      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

   elif status == '3':
      subject = 'Product Order Delivered'
      message = f''' Your Order is Delivered to the Location given.'''
      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

   elif status ==  '4':
      subject = 'Product Order Cancelled'
      message = f''' Your Order is Cancelled your transaction will be rolled back.'''
      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)
