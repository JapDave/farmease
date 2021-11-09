from django.db import models
from django.core.validators import RegexValidator ,FileExtensionValidator
import uuid
from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import binascii
import os

class ParanoidModelManager(models.Model):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class CategoryField(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("Category-Name"),max_length=50)
    
    class Meta:
        abstract = True


class Categories(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    gu = models.EmbeddedField(
        model_container= CategoryField
    )
    en = models.EmbeddedField(
        model_container=CategoryField
    )

    image = models.ImageField(("Profile Photo"), upload_to='category',validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])],height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()   

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) :
        return self.en.name 

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Categories, self).delete()
        else:
            self.deleted_at = now()
            self.save()

class FarmerField(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("Name"), max_length=50)
    state = models.CharField(("State"), max_length=20)
    district = models.CharField(("District"), max_length=20,)
    village = models.CharField(("Village"), max_length=20)
    postal_address = models.TextField(("Postal Address"))
   

    class Meta:
        abstract = True


class Farmer(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    gu = models.EmbeddedField(
        model_container= FarmerField
    )
    en = models.EmbeddedField(
        model_container=FarmerField
    )
    email = models.EmailField(("Email"), max_length=54,unique=True)
    password = models.CharField(("Password"), max_length=64)
    profile_photo = models.ImageField(("Profile Photo"), upload_to='farmer',validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])],height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    contact = models.CharField(("Contact No"),validators=[phoneNumberRegex],max_length=10,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()   

    class Meta:
        verbose_name_plural = "farmers"
        
    def __str__(self):
        return self.email

    def is_authenticated(self):
        return True

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Farmer, self).delete(**kwargs)
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

   

class ProductField(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("Name"), max_length=50, null=False, blank=False)
    description = models.TextField(("Description"),null=False, blank=False)


class Products(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,verbose_name=("Farmer"))
    category = models.ForeignKey(Categories,on_delete=models.CASCADE, verbose_name=("Category"))  
    gu = models.EmbeddedField(
        model_container= ProductField
    )
    en = models.EmbeddedField(
        model_container=ProductField
    )
    image = models.ImageField(("Image"), upload_to='Product', height_field=None, width_field=None,validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])] ,max_length=None)
    price = models.PositiveIntegerField(("Price"),null=False, blank=False)
    stock = models.PositiveIntegerField(("Stock"),null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()

    class Meta:
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Products, self).delete()
        else:
            self.deleted_at = now()
            self.save()


