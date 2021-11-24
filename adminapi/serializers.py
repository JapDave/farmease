from rest_framework import  serializers as restserial
from .models import SubAdmin,Token
from django.utils.translation import gettext_lazy as _
from rest_meets_djongo import serializers
from rest_framework.response import Response
from rest_framework import status
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
               user_obj=SubAdmin.objects.get(email=email)
            
            except:
                 msg = {'detail': 'user is not  registered.'}
                 raise restserial.ValidationError(msg)

            if user_obj and user_obj.password == hashlib.sha256(str.encode(password)).hexdigest():
                user = user_obj
             
            else:
                msg = {'detail': 'wrong password'}
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


class AdminSerializer(serializers.DjongoModelSerializer):

   class Meta:
      model = SubAdmin
      exclude = ['deleted_at']


class TokenSerializer(serializers.DjongoModelSerializer):
    user = AdminSerializer(SubAdmin.objects.all())

    class Meta:
        model = Token
        fields = ('key','user')

