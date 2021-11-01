from rest_framework import  serializers
from .models import Farmer, Products, Token
from django.utils.translation import gettext_lazy as _


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = False

        if email and password:
            try:
               user_obj=Farmer.objects.get(email=email)
            
            except:
                 msg = {'detail': 'user is not  registered.'}
                 raise serializers.ValidationError(msg)

            if user_obj and user_obj.password == password:
                user = user_obj
             
            else:
                msg = {'detail': 'user is not  registered.',
                    'register': False}
                raise serializers.ValidationError(msg)

            if user == False:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')
    
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Farmer
        exclude = ['deleted_at']
        extra_kwargs = {
            'password':{'write_only': True},
        }
      

class FarmerSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Farmer
        # fields = '__all__'
        exclude = ['deleted_at']

class TokenSerializer(serializers.ModelSerializer):
    user = FarmerSerializer(Farmer.objects.all())

    class Meta:
        model = Token
        fields = ('key','user')

class ProductSerializer(serializers.ModelSerializer):   
    # farmers = FarmerSerializer(Farmer.objects.all())
    # farmer = farmers.name
    class Meta:
        model = Products
        exclude = ['created_at','updated_at','deleted_at']