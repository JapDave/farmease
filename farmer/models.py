from enum import unique
from django.db import models
from django.core.validators import RegexValidator ,FileExtensionValidator,MinValueValidator,MaxValueValidator
import uuid
from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import binascii
import os
# from django_measurement.models import MeasurementField

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class CategoryField(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("Category Name"),max_length=50,unique=True)
    
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

class State(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("State"), max_length=50,unique=True)

    def __str__(self):
        return self.name

class District(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(("District"), max_length=50,unique=True)

    def __str__(self):
        return self.name

class Farmer(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(("First Name"), max_length=50)  
    last_name = models.CharField(("Last Name"), max_length=50)  
    email = models.EmailField(("Email"), max_length=54,unique=True)
    password = models.CharField(("Password"), max_length=64)
    profile_photo = models.ImageField(("Profile Photo"), upload_to='farmer',validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])],height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    contact = models.CharField(("Contact No"),validators=[phoneNumberRegex],max_length=10,unique=True)
    age = models.PositiveIntegerField(("Age"),blank=False)
    gender = models.CharField(("Gender"), max_length=50,blank=False)
    state = models.ForeignKey(State, verbose_name=_("State"), on_delete=models.CASCADE)
    district = models.ForeignKey(District, verbose_name=_("District"), on_delete=models.CASCADE)
    # village = models.CharField(("Village"), max_length=20)
    pin_code =  models.PositiveIntegerField(("Pincode"), validators=[MinValueValidator(111111), MaxValueValidator(999999)])
    postal_address = models.TextField(("Postal Address"))
    customer_capacity = models.PositiveIntegerField(_("Customer Capacity"),default=2147483647,validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    CHOICES = [('0','pending'),('1','active')]
    status = models.CharField(("Status"), choices=CHOICES,max_length=50,default='0') 
    objects = ParanoidModelManager()   

    class Meta:
        verbose_name_plural = "farmers"
        
    def __str__(self):
        return self.first_name

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
  
    # stock = MeasurementField(measurement=kilogram)

    class Meta:
        abstract = True

    # def __str__(self):
    #     return self._id

class Products(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.ForeignKey(Farmer,on_delete=models.CASCADE,verbose_name=("Farmer"))
    category = models.ForeignKey(Categories,on_delete=models.CASCADE, verbose_name=("Category")) 
    image = models.ImageField(("Image"), upload_to='Product', height_field=None, width_field=None,validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])] ,max_length=None) 
    price = models.PositiveIntegerField(("Price"),null=False, blank=False)
    stock = models.PositiveIntegerField(("Stock"),null=False, blank=False)
    gu = models.EmbeddedField(model_container= ProductField)
    en = models.EmbeddedField(model_container=ProductField)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()

    class Meta:
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.en.name

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Products, self).delete()
        else:
            self.deleted_at = now()
            self.save()


