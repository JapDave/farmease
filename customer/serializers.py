from farmer.models import Products,State,District
from farmer.serializers import DistrictSerializer, FarmerSerializer, ProductSerializer, StateSerializer
from rest_framework import  serializers as restserial
from .models import Cart, CartField, Customer, Order, OrderField, Token, Address
from django.utils.translation import gettext_lazy as _
from rest_meets_djongo import serializers
import uuid
import hashlib
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

            if user_obj and user_obj.password == hashlib.sha256(str.encode(password)).hexdigest():
                user = user_obj
             
            else:
                msg = {'detail': 'user password wrong '}
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
    pin_code = restserial.IntegerField(max_value=None, min_value=1)
    postal_address = restserial.CharField()


    class Meta:
        model = Customer
        exclude = ['deleted_at']
        extra_kwargs = {
            'password':{'write_only': True},
        }
        depth:1

    def create(self,validated_data): 
        pin_code = validated_data.pop('pin_code')
        postal_address = validated_data.pop('postal_address')
        address_obj = Address(pin_code=pin_code,postal_address=postal_address)
        address_obj.save()
        customer_obj = Customer(**validated_data)
        customer_obj.addresses.append(address_obj)
        customer_obj.save()
        return customer_obj
           

class CustomerSerializer(serializers.DjongoModelSerializer):
    farmer = FarmerSerializer()
    state = StateSerializer()
    district = DistrictSerializer()

    class Meta:
        model = Customer
        exclude = ['deleted_at']
        depth:2

    def update_data(self,instance,data):
        state = State.objects.get(_id=data.get('state'))
        district = District.objects.get(_id=data.get('district'))   
        return super().save(state=state,district=district)

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
   

class OrderFieldSerializer(serializers.DjongoModelSerializer):
  
    class Meta:
        model = OrderField
        fields = '__all__'
        depth = 3

class OrderSerializer(serializers.DjongoModelSerializer):

    items = OrderFieldSerializer(many=True, read_only=True) 
       
    class Meta:
        model = Order
        exclude = ['deleted_at']
        depth = 5

             
class TokenSerializer(serializers.DjongoModelSerializer):
    user = CustomerSerializer(Customer.objects.all())

    class Meta:
        model = Token
        fields = ('key','user')
