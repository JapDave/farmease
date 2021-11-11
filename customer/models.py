from django.db import models
from django.core.validators import RegexValidator ,FileExtensionValidator,MinValueValidator,MaxValueValidator
import uuid
from djongo import models 
# from farmer.models import Token
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import binascii
import os


class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class Address(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # customer = models.ForeignKey(Customer, verbose_name=("User"), on_delete=models.CASCADE,related_name='address')
    state = models.CharField(("State"), max_length=30)
    city = models.CharField(("City"), max_length=30)
    pin_code =  models.PositiveIntegerField(("Pincode"), validators=[MinValueValidator(111111), MaxValueValidator(999999)])
    postal_address = models.TextField(("Postal Address"))
    # objects = models.DjongoManager()   

    class Meta:
           verbose_name_plural = "Address"
           abstract=True


    def __str__(self):
        return self.postal_address +', '+self.city +', '+ self.state 
    

class CustomerField(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("Name"), max_length=50)
    addresses = models.ArrayField(model_container=Address, verbose_name=("Addresses"))
    
    class Meta:
        abstract=True


class Customer(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gu = models.EmbeddedField(model_container=CustomerField)
    en = models.EmbeddedField(model_container=CustomerField)
    password = models.CharField(("Password"), max_length=64)
    email = models.EmailField(("Email"), max_length=54,unique=True)
    profile_photo = models.ImageField(("Profile Photo"), upload_to='Customer', height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    contact = models.CharField(("Contact No"),validators=[phoneNumberRegex],max_length=10,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()   


    class Meta:
        verbose_name_plural = "Customers"
        
    def __str__(self):
        return self.en.name


    def is_authenticated(self):
        return True

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Customer, self).delete()
        else:
            self.deleted_at = now()
            self.save()



class Token(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(_("Key"), max_length=40, unique=True)
    user = models.ForeignKey(
       Customer, related_name='users',
        on_delete=models.CASCADE, verbose_name=_("Customer")
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
   
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Token, self).delete()
        else:
            self.deleted_at = now()
            self.save()