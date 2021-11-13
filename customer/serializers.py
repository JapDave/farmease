from rest_framework import  serializers as restserial
from .models import Customer, Token, Address
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
        

class TokenSerializer(serializers.DjongoModelSerializer):
    user = CustomerSerializer(Customer.objects.all())

    class Meta:
        model = Token
        fields = ('key','user')
