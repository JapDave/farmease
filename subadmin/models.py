from django.db import models
from django.core.validators import RegexValidator ,FileExtensionValidator,MinValueValidator
import uuid
from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
import binascii
import os
from farmer.models import State,District,ParanoidModelManager

class SubAdmin(models.Model):
   _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   name = models.CharField(("Name"), max_length=50)  
   email = models.EmailField(("Email"), max_length=54,unique=True)
   password = models.CharField(("Password"), max_length=64)
   profile_photo = models.ImageField(("Profile Photo"), upload_to='farmer',validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])],height_field=None, width_field=None, max_length=None)
   phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
   contact = models.CharField(("Contact No"),validators=[phoneNumberRegex],max_length=10,unique=True)
   state = models.ForeignKey(State, verbose_name=_("State"), on_delete=models.CASCADE)
   district = models.ForeignKey(District, verbose_name=_("District"), on_delete=models.CASCADE)
   postal_address = models.TextField(("Postal Address"))
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
   objects = ParanoidModelManager()   

   class Meta:
        verbose_name_plural = "Admin"
        
   def __str__(self):
      return self.name

   def is_authenticated(self):
      return True

   def delete(self, hard=False, **kwargs):
      if hard:
         super(SubAdmin, self).delete(**kwargs)
      else:
         self.deleted_at = now()
         self.save()


class Token(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(_("Key"), max_length=40, unique=True)
    user = models.ForeignKey(
       SubAdmin,related_name='Admin',
        on_delete=models.CASCADE, verbose_name=_("Admin")
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
