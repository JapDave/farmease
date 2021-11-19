from customer.serializers import CustomerSerializer
from rest_framework import generics, permissions
from .serializers import *
from customer.serializers import OrderSerializer,OrderFieldSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_auth.views import LoginView as RestLoginView
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from .paginations import ProductPagination,CustomerPagination
from customer.paginations import OrderPagination
from customer.models import Customer, Order
from .tasks import  mail_user_updateorder
import random
from django.conf import settings
from django.core.mail import send_mail
import  hashlib

class GetMaster(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self,request):
        category_serial = CategorySerializer(Categories.objects.all(), many=True)
        state_serial = StateSerializer(State.objects.all(), many=True)
        district_serial = DistrictSerializer(District.objects.all(), many=True)
        return Response({'result':{'categories':category_serial.data,
                                    'states':state_serial.data,
                                    'district':district_serial.data}},status=status.HTTP_201_OK)


class ForgotPassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        try:
            email = request.POST['email']
            farmer_obj = Farmer.objects.get(email=email)
            generated_otp = random.randint(1111, 9999)
            request.session['user'] = str(farmer_obj._id)
            request.session['otp'] = generated_otp
            subject = 'Acount Recovery'
            message = f'''your otp for account recovery is {generated_otp}'''
            email_from = settings.EMAIL_HOST_USER
            recepient = [farmer_obj.email, ]
            send_mail(subject, message, email_from, recepient)
            return Response({'detail':'Otp Sent To Email'},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Error To Get Registered Farmer '},status=status.HTTP_400_BAD_REQUEST)


class OtpVerification(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        try:
            user_otp = request.POST['otp']
            if user_otp == str(request.session.get('otp')):
                del request.session['otp']
                return Response({'detail':'Otp Verified'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Wrong Otp'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail':'Error To Verify Otp'},status=status.HTTP_404_NOT_FOUND)

class ChangePassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        try:
            if not request.session.get('otp'):
                new_password = request.POST['new_password']
                confirm_password = request.POST['confirm_password']
                
                if new_password == confirm_password:
                    farmer_obj = Farmer.objects.get(_id = str(request.session.get('user')))
                    farmer_obj.password = hashlib.sha256(str.encode(new_password)).hexdigest()
                    farmer_obj.save()
                    del request.session['user']
                    return Response({'detail':'Password Changed Successfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'detail':'Password Not Matched'},status=status.HTTP_400_BAD_REQUEST)
            else:
                    return Response({'detail':'Cannot Change Password Without otp verification '},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
        
            return Response({'detail':'Password Not Changed'},status=status.HTTP_404_NOT_FOUND)


class ProfileChangePassword(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self,request,farmer_id):
        try:
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            
            if new_password == confirm_password:
                farmer_obj = Farmer.objects.get(_id = farmer_id)
                farmer_obj.password = hashlib.sha256(str.encode(new_password)).hexdigest()
                farmer_obj.save()
                return Response({'detail':'Password Changed Successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Password Not Matched'},status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:         
            return Response({'detail':'Password Not Changed'},status=status.HTTP_404_NOT_FOUND)



class Login(RestLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_response_serializer(self):

        response_serializer = TokenSerializer
        return response_serializer

    def get_response(self,user,request):
        serializer_class = self.get_response_serializer()
        token_create = Token.objects.create(user=user)
        request.session['token_id'] = str(token_create._id)
        serializer = serializer_class(token_create,
                                            context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return self.get_response(user,request)


class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args,  **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()
            user = serializer.save()
            return Response({
                "user": FarmerSerializer(user,context=self.get_serializer_context()).data,
                "message": "Farmer Created Successfully.  Now perform Login to get your token",
            })
        except Exception as e:
         
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    authentication_classes = (TokenAuthentication,)
    def post(self, request, *args, **kwargs):
        
        return self.logout(request)

    def logout(self, request):
        try:
           token_obj = Token.objects.get(_id=request.session.get('token_id'))
           token_obj.delete()
           del request.session['token_id']
        except (AttributeError, ObjectDoesNotExist):
            pass
       
        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
      
        return response

class Profile(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        try:
            profile = Farmer.objects.get(_id=request.user._id)         
            serializer = FarmerSerializer(profile)
            return Response(serializer.data)
        except:
            return Response({'detail':'Farmer Does Not Exsits'},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):       
        instance = Farmer.objects.get(_id=request.user._id)
        serializer = FarmerSerializer(instance,data=request.data)   
        if serializer.is_valid():
            serializer.update_data(instance,request.data)
            return Response({'detail':'Profile Updated'},status=status.HTTP_201_CREATED)
        else:
           return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
       
         
class AddProduct(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:
            serializer = AddProductSerializer(data=request.data)
            serializer.is_valid()
            result =  serializer.create(request)
            if result == True:
                return Response({'detail':'Product Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':result},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class AllProducts(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    page_size = 1
    page = 1
  
    def get(self,request):     
        product_data = Products.objects.filter(farmer___id=request.user._id)
        if product_data.count() > 0:
            page = self.paginate_queryset(product_data)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(product_data, many=True)
            return Response(serializer.data)

        else:
            return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)
    
       
class ProductDetail(generics.GenericAPIView):

    authentication_classes = (TokenAuthentication,)

    def get(self,request,id):
        try:
            serializer = ProductSerializer(Products.objects.get(_id=id))
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Product Not Found'},status=status.HTTP_204_NO_CONTENT)

    def post(self,request,id):
        try:
            instance = Products.objects.get(_id=id)
            serializer = ProductSerializer(instance,data=request.data,partial=True)
            serializer.is_valid()       
            result = serializer.updateproduct(instance,request.data)
            try:
              
                serializer.update(instance,result)
                return Response({'detail':'Product Updated'},status=status.HTTP_201_CREATED)
            except:
                return Response({'detail':result},status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            Products.objects.get(_id=id).delete()       
            return Response({'detail':'Product Deleted'},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Product Already Deleted.'},status=status.HTTP_400_BAD_REQUEST)



class CustomerList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination
    page_size = 1
    page = 1

    def get(self,request):
        customer_data = Customer.objects.filter(farmer = request.user._id)
        if customer_data.count() > 0 :
            page = self.paginate_queryset(customer_data)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(customer_data, many=True)
            return Response(serializer.data)

        else:
            return Response({'detail':'error'})


class OrderList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    page_size = 1
    page = 1
    
    def get(self,request):
        try:
            order_obj = Order.objects.filter(farmer=request.user._id)        
            page = self.paginate_queryset(order_obj)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(order_obj, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail':'Error To Get Order History'},status=status.HTTP_404_NOT_FOUND)

class OrderDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = OrderFieldSerializer
    pagination_class = OrderPagination
    page_size = 1
    page = 1
    
    def get(self,request,order_id):
        try:
            order_obj = Order.objects.get(_id = order_id)
            if order_obj.items != []:
                page = self.paginate_queryset(order_obj.items)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(order_obj.items, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail':'Error To Get Product'},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,order_id):
        try:
            order_status = request.data['status']
            order_obj = Order.objects.get(_id=order_id)
            order_obj.status = order_status
            order_obj.save()
            if order_obj.status == '1':
                for item in order_obj.items:
                    item.product.en.stock -= item.qty 
                    item.product.gu.stock -= item.qty
                    item.product.save()
              
        
            mail_user_updateorder.delay(order_status,order_obj.customer.email,order_obj._id)
            serializer = OrderSerializer(order_obj)
            return Response({'detail':serializer.data},status=status.HTTP_200_OK)          
        except Exception as e:
            return Response({'detail':'Error To Change Status'},status=status.HTTP_404_NOT_FOUND)

   