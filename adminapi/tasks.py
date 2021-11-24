from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task(name='mail_sender_newadmin')
def mail_sender_newadmin(email,password):
   
   subject = 'New Account Registered'
   message = f''' Thank-you for registering into our site.
   Your Login link : http://127.0.0.1:8000/admin/login.
   email : {email}.
   password: {password}.
   '''
   email_from = settings.EMAIL_HOST_USER
   recepient  = [email,]
   send_mail(subject, message, email_from, recepient)
              