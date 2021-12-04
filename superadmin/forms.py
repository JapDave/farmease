from django import forms
from django.forms import fields
from django.forms.widgets import FileInput
from customer.models import Address, Customer,Order, OrderField
from farmer.models import Categories, District, Farmer, Products, State,FileExtensionValidator
from adminapi.models import SubAdmin
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField
from django.conf import settings


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class StateForm(forms.ModelForm):
    
    class Meta:
        model = State
        exclude = ['deleted_at']


class DistrictForm(forms.ModelForm):
    
    class Meta:
        model = District
        exclude = ['deleted_at']

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = '__all__'

#
class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):

        input_html = super().render(name, value, attrs={'onChange': 'upload_img(this);'}, **kwargs)
        if value:
            try:
                img_html = mark_safe(f'<img src="{value.url}" width="100px" height="100px" id="img_id2" style="visibility:visible;" /><br><br>')
                return f'{img_html}{input_html}'
            except:        
                img_html = mark_safe(f'<img src="#" width="0px" height="0px" id="img_id2" class="m-1" style="visibility:hidden;"/>')
                return f'{img_html}{input_html}'
        else:  
            img_html = mark_safe(f'<img src="#" id="img_id2" style="visibility:hidden;"/>')
            return f'{img_html}{input_html}'
       

class CategoryForm(forms.ModelForm):
    
    image = ImageField(widget=PictureWidget)
    class Meta:
        model = Categories
        exclude = ['addresses','deleted_at']

class AdminForm(forms.ModelForm):
   profile_photo = ImageField(widget=PictureWidget)
   class Meta:
      model = SubAdmin
      exclude = ['deleted_at']
      CHOICES = [('M','Male'),('F','Female')]
      widgets = {'gender':forms.RadioSelect(choices=CHOICES)}


class FarmerForm(forms.ModelForm):
    profile_photo = ImageField(widget=PictureWidget)
    class Meta:
        model = Farmer
        exclude = ['deleted_at']
        CHOICES = [('M','Male'),('F','Female')]
        widgets = {'gender':forms.RadioSelect(choices=CHOICES),
                    }

class CustomerForm(forms.ModelForm):

    profile_photo = ImageField(widget=PictureWidget)
    class Meta:
        model = Customer
        exclude = ['deleted_at']
        CHOICES = [('M','Male'),('F','Female')]
        widgets = {'gender':forms.RadioSelect(choices=CHOICES),
                     'password': forms.PasswordInput()}

class CustomerUpdateForm(forms.ModelForm):

    profile_photo = ImageField(widget=PictureWidget)
    class Meta:
        model = Customer
        exclude = ['deleted_at','addresses']
        CHOICES = [('M','Male'),('F','Female')]
        widgets = {'gender':forms.RadioSelect(choices=CHOICES)}


class ProductForm(forms.ModelForm):

    image = ImageField(widget=PictureWidget)
    class Meta:
        model = Products
        exclude = ['deleted_at']

class OrderFieldForm(forms.ModelForm):

    class Meta:
        model = OrderField
        exclude = ['_id']

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ['items','deleted_at']