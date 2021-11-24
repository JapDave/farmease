from django import forms
from django.forms import fields
from customer.models import Address, Customer,Order, OrderField
from farmer.models import Categories, District, Farmer, Products, State
from adminapi.models import SubAdmin




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
    

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Categories
        exclude = ['addresses','deleted_at']


class AdminForm(forms.ModelForm):
   
   class Meta:
      model = SubAdmin
      exclude = ['deleted_at']
      CHOICES = [('M','Male'),('F','Female')]
      widgets = {'gender':forms.RadioSelect(choices=CHOICES)}

class FarmerForm(forms.ModelForm):
   
   class Meta:
      model = Farmer
      exclude = ['deleted_at']
      CHOICES = [('M','Male'),('F','Female')]
      widgets = {'gender':forms.RadioSelect(choices=CHOICES)}

class CustomerForm(forms.ModelForm):
   
   class Meta:
      model = Customer
      exclude = ['deleted_at']
      CHOICES = [('M','Male'),('F','Female')]
      widgets = {'gender':forms.RadioSelect(choices=CHOICES)}

class ProductForm(forms.ModelForm):

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