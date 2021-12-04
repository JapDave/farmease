from customer.models import Order,Customer
from customer.views import Register
from farmer.models import Farmer, Products
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions
from customer.serializers import OrderSerializer,CustomerSerializer
from farmer.serializers import FarmerSerializer, ProductSerializer
from rest_auth.views import LoginView as RestLoginView
from .authentication import TokenAuthentication
from .serializers import TokenSerializer,LoginUserSerializer,AdminSerializer
from .models import SubAdmin, Token
from rest_framework.response import Response
from rest_framework import status
from .paginations import FarmerPagination
from customer.paginations import OrderPagination
from farmer.paginations import ProductPagination,CustomerPagination
import random
from django.conf import settings
from django.core.mail import send_mail
import hashlib
from farmer.views import Register as fr
from rest_framework.views import APIView


class ForgotPassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        try:
            email = request.POST['email']
            farmer_obj = SubAdmin.objects.get(email=email)
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
                    farmer_obj = SubAdmin.objects.get(_id = str(request.session.get('user')))
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

class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self, request, *args, **kwargs):
        try:
            token_obj = Token.objects.get(key=request.data['token'])
            token_obj.delete()
            # del request.session['token_id']
            response = Response({"success": "Successfully logged out."},
                            status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist): 
            response = Response({"error": "Already Logged Out"},
                            status=status.HTTP_400_BAD_REQUEST)
        return response

class FarmerRegister(fr):
    authentication_classes = (TokenAuthentication,)

class CustomerRegister(Register):
     authentication_classes = (TokenAuthentication,)

class ProfileChangePassword(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self,request,admin_id):
        try:
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            
            if new_password == confirm_password:
                admin_obj = SubAdmin.objects.get(_id = admin_id)
                admin_obj.password = hashlib.sha256(str.encode(new_password)).hexdigest()
                admin_obj.save()
                return Response({'detail':'Password Changed Successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Password Not Matched'},status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:      
            return Response({'detail':'Password Not Changed'},status=status.HTTP_404_NOT_FOUND)

class Profile(generics.GenericAPIView):
   authentication_classes = (TokenAuthentication,)
  

   def get(self, request):       
        serializer = AdminSerializer(request.user)
        return Response(serializer.data)

   def post(self, request):       
        serializer = AdminSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Profile Updated'},status=status.HTTP_201_CREATED)
        else:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class FarmerList(generics.GenericAPIView):
   
    authentication_classes = (TokenAuthentication,)
    serializer_class = FarmerSerializer
    pagination_class = FarmerPagination
    page_size = 10
    page = 1
  
    def get(self,request):     
        farmer_obj = Farmer.objects.filter(state = request.user.state)
        if farmer_obj.count() > 0:
            page = self.paginate_queryset(farmer_obj)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(farmer_obj, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        else:
            return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)


class CustomerList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination
    page_size = 10
    page = 1
  
    def get(self,request):     
        customer_obj = Customer.objects.filter(state = request.user.state)
        if customer_obj.count() > 0:
            page = self.paginate_queryset(customer_obj)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(customer_obj, many=True)
            return Response({'detail':serializer.data},status=status.HTTP_200_OK)

        else:
            return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)


class FarmerDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request,farmer_id):
        try:
            serializer = FarmerSerializer(Farmer.objects.get(_id=farmer_id,state=request.user.state))
            return Response({'farmer':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Error To Get Farmer Detail'},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,farmer_id):
        try:
            farmer_obj = Farmer.objects.get(_id=farmer_id,state=request.user.state)
            serializer = FarmerSerializer(farmer_obj,data=request.data,partial=True)
            serializer.is_valid()
            serializer.update(farmer_obj,serializer.validated_data)        
            return Response({'message':'Farmer Updated','farmer':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':'Error To Update Farmer'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,farmer_id):
        try:
            farmer_obj = Farmer.objects.get(_id=farmer_id)
            farmer_obj.delete()
            return Response({'success':'Farmer Deleted'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':'Farmer Not Deleted'},status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request,customer_id):
        try:
            serializer = CustomerSerializer(Customer.objects.get(_id=customer_id,state=request.user.state))
            return Response({'customer':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Error To Get Customer Detail'},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,customer_id):
        try:
            customer_obj = Customer.objects.get(_id=customer_id,state=request.user.state)
            serializer = CustomerSerializer(customer_obj,data=request.data,partial=True)
            serializer.is_valid()
            serializer.update_data(customer_obj,request.data)
            return Response({'message':'Customer Updated','Customer':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':'Error To Update Customer'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,farmer_id):
        try:
            customer_obj = Customer.objects.get(_id=farmer_id)
            customer_obj.delete()
            return Response({'success':'Customer Deleted'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':'Customer Not Deleted'},status=status.HTTP_400_BAD_REQUEST)


class ProductList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    page_size = 10
    page = 1
  
    def get(self,request):     
        product_obj = Products.objects.filter(farmer__state = request.user.state)
        if product_obj.count() > 0:
            page = self.paginate_queryset(product_obj)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(product_obj, many=True)
            return Response({'detail':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)

class ProductDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request,product_id):
        try:
            serializer = ProductSerializer(Products.objects.get(_id=product_id))
            return Response({'product':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Error To Get Product Detail'},status=status.HTTP_404_NOT_FOUND)

class OrderHistory(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    page_size = 10
    page = 1
  
    def get(self,request,farmer_id):     
        order_obj = Order.objects.filter(farmer = farmer_id)
        if order_obj.count() > 0:
            page = self.paginate_queryset(order_obj)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(order_obj, many=True)
            return Response({'detail':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"detail":"No Order Found."},status=status.HTTP_204_NO_CONTENT)

class OrderDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request,order_id):
        try:
            order_obj = Order.objects.get(_id=order_id)
            serializer = OrderSerializer(order_obj)
            return Response({'order':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'No Order Detail Found'},status=status.HTTP_400_BAD_REQUEST)