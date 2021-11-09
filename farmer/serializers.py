from rest_framework import  serializers as restserial
from .models import Categories, CategoryField, Farmer, FarmerField, Products, Token
from django.utils.translation import gettext_lazy as _
from rest_meets_djongo import serializers

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

class FarmerFieldSerializer(serializers.EmbeddedModelSerializer):
    
    class Meta:
        model = FarmerField
        fields = '__all__'

class CategoryFieldSerializer(serializers.EmbeddedModelSerializer):
    
    class Meta:
        model = CategoryField
        fields = '__all__'


class RegisterSerializer(serializers.DjongoModelSerializer):
    gu = FarmerFieldSerializer()
    en = FarmerFieldSerializer()

    class Meta:
        model = Farmer
        exclude = ['deleted_at']
        extra_kwargs = {
            'password':{'write_only': True},
        }
      
class CategorySerializer(serializers.DjongoModelSerializer):

    class Meta:
        model = Categories
        exclude = ('deleted_at',)


class FarmerSerializer(serializers.DjongoModelSerializer):
    gu = FarmerFieldSerializer()
    en = FarmerFieldSerializer()

    class Meta:
        model = Farmer
        exclude = ['deleted_at']


class TokenSerializer(serializers.DjongoModelSerializer):
    user = FarmerSerializer(Farmer.objects.all())

    class Meta:
        model = Token
        fields = ('key','user')


class AddProductSerializer(serializers.DjongoModelSerializer):   
  
    class Meta:
        model = Products
        exclude = ('deleted_at',)


class ProductSerializer(serializers.DjongoModelSerializer):   
    category = CategorySerializer(Categories.objects.all())
    
    class Meta:
        model = Products
        exclude = ['farmer','deleted_at']