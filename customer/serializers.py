from django.core.validators import integer_validator
from django.db.models import fields
from farmer.models import Products
from farmer.serializers import ProductSerializer
from rest_framework import  serializers as restserial
from .models import Cart, CartField, Customer, Order, OrderField, Token, Address
from django.utils.translation import gettext_lazy as _
from rest_meets_djongo import serializers
import uuid
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.com',])



class LoginUserSerializer(restserial.Serializer):
    email = restserial.EmailField()
    password = restserial.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = False

        if email and password:
            try:
               user_obj=Customer.objects.get(email=email)
            
            except:
                 msg = {'detail': 'user is not  registered.'}
                 raise restserial.ValidationError(msg)

            if user_obj and user_obj.password == password:
                user = user_obj
             
            else:
                msg = {'detail': 'user is not  registered.',
                    'register': False}
                raise restserial.ValidationError(msg)

            if user == False:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise restserial.ValidationError(msg, code='authorization')
    
        else:
            msg = 'Must include "username" and "password".'
            raise restserial.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class AddressSerializer(serializers.EmbeddedModelSerializer):
    _id = restserial.UUIDField(default=uuid.uuid4)
    class Meta:
        model = Address
        fields = '__all__'
        # depth = 1

class RegisterSerializer(serializers.DjongoModelSerializer):
    # addresses = AddressSerializer()

    class Meta:
        model = Customer
        exclude = ['farmer','deleted_at']
        extra_kwargs = {
            'password':{'write_only': True},
        }
        


class CustomerSerializer(serializers.DjongoModelSerializer):
    # addresses = AddressSerializer()
  
    class Meta:
        model = Customer
        exclude = ['deleted_at']


class CartFieldSerializer(serializers.EmbeddedModelSerializer):
    # product = ProductSerializer()
    class Meta:
        model = CartField
        fields = '__all__'
        depth = 1

class CartSerializer(serializers.DjongoModelSerializer):
    
    class Meta:
        model = Cart
        exclude = ['user','deleted_at'] 
        depth = 1

class QtySerializer(restserial.Serializer):
    qty = restserial.IntegerField(max_value=None, min_value=1) 
   

class OrderFieldSerializer(serializers.EmbeddedModelSerializer):
    _id = restserial.UUIDField(default=uuid.uuid4)

    class Meta:
        model = OrderField
        fields = '__all__'

class OrderSerializer(serializers.DjongoModelSerializer):
    class Meta:
        model = Order
        exclude = ['deleted_at']
     


class TokenSerializer(serializers.DjongoModelSerializer):
    user = CustomerSerializer(Customer.objects.all())

    class Meta:
        model = Token
        fields = ('key','user')
