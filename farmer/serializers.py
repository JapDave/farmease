from rest_framework import  serializers as restserial
from .models import Categories, CategoryField, Farmer, ProductField, Products, Token
from django.utils.translation import gettext_lazy as _
from rest_meets_djongo import serializers
from rest_framework.response import Response
from rest_framework import status
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
               user_obj=Farmer.objects.get(email=email)
            
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



class CategoryFieldSerializer(serializers.EmbeddedModelSerializer):
    
    class Meta:
        model = CategoryField
        fields = '__all__'

class ProductFieldSerializer(serializers.EmbeddedModelSerializer):
    
    class Meta:
        model = ProductField
        fields = '__all__'

class RegisterSerializer(serializers.DjongoModelSerializer):
  
    class Meta:
        model = Farmer
        exclude = ['deleted_at']
        extra_kwargs = {
            'password':{'write_only': True},
        }
      
class CategorySerializer(serializers.DjongoModelSerializer):

    class Meta:
        model = Categories
        exclude = ['deleted_at']


class FarmerSerializer(serializers.DjongoModelSerializer):

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
        exclude = ['farmer','deleted_at']

    def create(self, request):
        lan = request.data.get('language_selected')
        category = Categories.objects.get(_id=request.data.get('category'))
        farmer = Farmer.objects.get(_id=request.user._id)
        image = request.data.get('image')
        request.data.pop('language_selected')
        request.data.pop('category')
        request.data.pop('image')
       
       
        if lan == 'gu':
            obj_serializer1 = ProductFieldSerializer(data=request.data)
            if obj_serializer1.is_valid():
                obj1 = ProductField(**request.data.dict())
                obj1.save()
                for key,value in request.data.items():
                    request.data[key] = translator.translate(value,dest='en').text
                obj2 = ProductField(**request.data.dict())
                obj2.save()        
                product_obj = Products(en=obj2,gu=obj1,category=category,farmer=farmer,image=image)       
                product_obj.save()
                return True
            else:
                return obj_serializer1.errors
        else:
            obj_serializer1 = ProductFieldSerializer(data=request.data)
            if obj_serializer1.is_valid():
                obj1 = ProductField(**request.data.dict())
                obj1.save()
                for key,value in request.data.items():
                    request.data[key] = translator.translate(value,dest='gu').text
                obj2 = ProductField(**request.data.dict())
                obj2.save()        
                product_obj = Products(en=obj1,gu=obj2,category=category,farmer=farmer,image=image)       
                product_obj.save()
                return True
            else:
                return obj_serializer1.errors
        
                
class ProductSerializer(serializers.DjongoModelSerializer):   
  

    class Meta:
        model = Products
        exclude = ['farmer','deleted_at']
        depth = 1

    def updateproduct(self,instance,data):
        result = {}
        lan = data.get('language_selected')
        category_id = data.get('category')
        if category_id:
            category = Categories.objects.get(_id=category_id)
            data.pop('category')
            result['category'] = category
            
        image = data.get('image')
        data.pop('language_selected')     
        data.pop('image')
        result['image'] = image
       
       
        if lan == 'gu':
            obj_serializer1 = ProductFieldSerializer(instance.gu,data=data,partial=True)
            if obj_serializer1.is_valid():
                obj_serializer1.update(instance.gu,data)
                result['gu'] = data
                new_data = {}
                for key,value in data.items():
                    new_data[key] = translator.translate(value,dest='en').text
                
                obj_serializer2 = ProductFieldSerializer(instance.en,data=new_data,partial=True)
                obj_serializer2.update(instance.en,new_data)   
                result['en'] = new_data
                return result
            else:
                return obj_serializer1.errors
        else:
            obj_serializer1 = ProductFieldSerializer(instance.en,data=data,partial=True)
            if obj_serializer1.is_valid():
                obj_serializer1.update(instance.en,data)
                result['en'] = data
                new_data = {}
                for key,value in data.items():
                    new_data[key] = translator.translate(value,dest='gu').text
                
                obj_serializer2 = ProductFieldSerializer(instance.gu,data=new_data,partial=True)
                obj_serializer2.update(instance.gu,new_data)   
                result['gu'] = new_data
                return result
            else:
                return obj_serializer1.errors
      