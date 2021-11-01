from django.db import models
from django.core.validators import RegexValidator ,FileExtensionValidator
import uuid
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import binascii
import os

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)


class Categories(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(("Category-Name"),max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()

    def __str__(self) :
        return self.category_name 

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Categories, self).delete()
        else:
            self.deleted_at = now()
            self.save()

class Farmer(models.Model ):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("Name"), max_length=50)  
    email = models.EmailField(("Email"), max_length=254,unique=True)
    password = models.CharField(("Password"), max_length=64)
    profile_photo = models.ImageField(("Profile Photo"), upload_to='farmer', height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    contact = models.CharField(("Contact No"),validators=[phoneNumberRegex],max_length=10,unique=True)
    state = models.CharField(("State"), max_length=50)
    district = models.CharField(("district"), max_length=50)
    village = models.CharField(("village"), max_length=50)
    postal_address = models.TextField(("Postal Address"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()   

    class Meta:
        verbose_name = 'farmers'
        
    def __str__(self):
        return self.name

    def is_authenticated(self):
        return True

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Farmer, self).delete()
        else:
            self.deleted_at = now()
            self.save()

class Token(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(_("Key"), max_length=40, unique=True)
    user = models.ForeignKey(
       Farmer,related_name='users',
        on_delete=models.CASCADE, verbose_name=_("farmer")
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

   
class Products(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,null=True,blank=True,verbose_name=("Owner") )
    category = models.ForeignKey(Categories,on_delete=models.CASCADE, verbose_name=("Category"))
    product_name = models.CharField(("Name"), max_length=50, null=False, blank=False)
    img = models.ImageField(("Image"), upload_to='Product', height_field=None, width_field=None,validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])] ,max_length=None)
    price = models.PositiveIntegerField(("Price"))
    description = models.TextField(("Description"))
    stock = models.PositiveIntegerField(("Stock"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()

    class Meta:
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.product_name

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Products, self).delete()
        else:
            self.deleted_at = now()
            self.save()