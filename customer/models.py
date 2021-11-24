from django.db import models
from django.core.validators import RegexValidator ,FileExtensionValidator,MinValueValidator,MaxValueValidator
import uuid
from djongo import models 
from farmer.models import Farmer, State,District,Categories
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import binascii
import os

from farmer.models import Products

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class Address(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pin_code =  models.PositiveIntegerField(("Pincode"), validators=[MinValueValidator(111111), MaxValueValidator(999999)])
    postal_address = models.TextField(("Postal Address"))
    objects = models.DjongoManager()

    class Meta:
        abstract = True
    
class Customer(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(("FirstName"), max_length=50) 
    last_name = models.CharField(("LastName"), max_length=50) 
    password = models.CharField(("Password"), max_length=64)
    email = models.EmailField(("Email"), max_length=54,unique=True)
    profile_photo = models.ImageField(("Profile Photo"), upload_to='Customer', height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    contact = models.CharField(("Contact No"),validators=[phoneNumberRegex],max_length=10,unique=True)
    age = models.PositiveIntegerField(("Age"),blank=False)
    gender = models.CharField(("Gender"), max_length=50,blank=False)
    state = models.ForeignKey(State, verbose_name=_("State"), on_delete=models.CASCADE)
    district = models.ForeignKey(District, verbose_name=_("District"), on_delete=models.CASCADE)
    addresses = models.ArrayField(model_container=Address, verbose_name=("Addresses"),null=True,blank=True,default=[])
    farmer = models.ForeignKey(Farmer, verbose_name=("Farmer"), on_delete=models.CASCADE,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()   

    class Meta:
        verbose_name_plural = "Customers"
        
    def __str__(self):
        return self.first_name

    def is_authenticated(self):
        return True

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Customer, self).delete()
        else:
            self.deleted_at = now()
            self.save()



class CartField(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, verbose_name=("Product-item"), on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(("product_qty"),default=1)

    class Meta:
        abstract = True

class Cart(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Customer, verbose_name=("user"), on_delete=models.CASCADE)
    item = models.ArrayField(CartField,verbose_name=("Items"),null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()

    class Meta:
           verbose_name_plural = "Cart"
        
 
    def delete(self, hard=False, **kwargs):
        if hard:
            super(Cart, self).delete()
        else:
            self.deleted_at = now()
            self.save()
    
    def __str__(self):
        return self.user.name

class OrderField(models.Model):
    _id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    product = models.ForeignKey(Products, verbose_name=_("Products"), on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(("Product-qty"),default=1) 
   
    objects = models.DjongoManager()

    class Meta:
        abstract = True
    

class Order(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=("Customer"), on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, verbose_name=("Farmer"), on_delete=models.CASCADE,default=None)
    items = models.ArrayField(OrderField, verbose_name=("Items"),default=None)  
    total = models.PositiveIntegerField(("Total-Amount"))
    address = models.EmbeddedField(Address)
    CHOICES = [('0','Pending'),('1','Approved'),('2','Dispatched'),('3','Delievered'),('4','Cancelled')]
    status = models.CharField(("status"),choices=CHOICES, max_length=50,default='0')
    CHOICES1 = [('0','COD'),('1','ONLINE')]
    payment_method = models.CharField(("Payment-Method"),choices=CHOICES1 ,max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()


    def delete(self, hard=False, **kwargs):
        if hard:
            super(Order, self).delete()
        else:
            self.deleted_at = now()
            self.save()

    def __str__(self):
        return self.customer.first_name


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