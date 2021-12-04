from django.db import reset_queries
from customer.tasks import mail_sender_farmer, mail_sender_user
from farmer.models import Farmer,Products
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import AddressSerializer, OrderFieldSerializer, OrderSerializer, QtySerializer, RegisterSerializer, CustomerSerializer,TokenSerializer,LoginUserSerializer,CartFieldSerializer
from farmer.serializers import CategorySerializer,StateSerializer,DistrictSerializer,FarmerSerializer,ProductSerializer
from .models import Cart, Customer, Order, Token, State, District,Categories
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_auth.views import LoginView as RestLoginView
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from .paginations import CartPagination, OrderPagination
from farmer.paginations import ProductPagination
import random
from django.conf import settings
from django.core.mail import send_mail
import hashlib




class GetMaster(generics.GenericAPIView):
    def get(self,request):
        category_serial = CategorySerializer(Categories.objects.all(), many=True)
        state_serial = StateSerializer(State.objects.all(), many=True)
        district_serial = DistrictSerializer(District.objects.all(), many=True)
        return Response({'result':{'categories':category_serial.data,
                                    'states':state_serial.data,
                                    'district':district_serial.data}},status=status.HTTP_200_OK)

class ForgotPassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        try:
            email = request.POST['email']
            farmer_obj = Customer.objects.get(email=email)
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
                    farmer_obj = Customer.objects.get(_id = str(request.session.get('user')))
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
    
    def post(self,request,customer_id):
        try:
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            
            if new_password == confirm_password:
                customer_obj = Customer.objects.get(_id = customer_id)
                customer_obj.password = hashlib.sha256(str.encode(new_password)).hexdigest()
                customer_obj.save()
                return Response({'detail':'Password Changed Successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Password Not Matched'},status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:         
            return Response({'detail':'Password Not Changed'},status=status.HTTP_404_NOT_FOUND)


class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)     
        serializer.is_valid(raise_exception=True)      
        result  =  serializer.create(serializer.validated_data)
        if result != None:
            return Response({
                "user": CustomerSerializer(result).data,
                "message": "Customer Created Successfully.  Now perform Login to get your token",
            })
        else:
            return Response({'detail':'Customer Not Created'},status=status.HTTP_400_BAD_REQUEST)


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
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data)

   def post(self, request):       
        serializer = CustomerSerializer(request.user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Profile Updated'},status=status.HTTP_201_CREATED)
        else:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class AddressView(generics.GenericAPIView):
        authentication_classes = (TokenAuthentication,)

        def get(self,request):
            try:
                # customer_obj = Customer.objects.get(_id=customer_id)
                serializer = AddressSerializer(request.user.addresses,many=True)
                return Response({'Addresses':serializer.data},status=status.HTTP_200_OK)
            except:
                return Response({'detail':'No Address Found'},status=status.HTTP_400_BAD_REQUEST)

class AddressDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
   
    def get(self,request,address_id):
        customer_obj = Customer.objects.get(_id=request.user._id)
        for add in customer_obj.addresses:
            if str(add._id) == address_id:
                data = add
                break
        try:
            serializer = AddressSerializer(data)
            return Response({'Address':serializer.data},status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({'detail':'Error To Get Data'},status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self,request,address_id):
        customer_obj = Customer.objects.get(_id=request.user._id)
        for add in customer_obj.addresses:
            if str(add._id) == address_id:
                data = add
                break
        try:
            customer_obj.addresses.remove(data)
            customer_obj.save()
            return Response({'detail':'Address Deleted'},status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({'detail':'Error To Get Data'},status=status.HTTP_400_BAD_REQUEST) 
    
    def post(self,request,address_id):
        customer_obj = Customer.objects.get(_id=request.user._id)
       
        for add in customer_obj.addresses:
            counter = 0
            if str(add._id) == address_id:
                address_serial = AddressSerializer(add,request.data,partial=True)
                address_serial.is_valid()
                address_obj = address_serial.save()
                try:
                    customer_obj.addresses[counter] = address_obj
                    customer_obj.save()
                    return Response({'detail':'Address updated'},status=status.HTTP_200_OK) 
                except Exception as e:
                    
                    return Response({'detail':'Error To update Data'},status=status.HTTP_400_BAD_REQUEST) 
            counter = +1


class AddAddress(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    
    def post(self,request):
        try:
            # customer_obj = Customer.objects.get(_id=customer_id)
            address_serializer = AddressSerializer(data=request.data)
            if address_serializer.is_valid():              
                address_obj = address_serializer.save()
                request.user.addresses.append(address_obj)
                request.user.save()
                return Response({'detail':'Address Added Successfully',
                                'address':address_serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':address_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'detail':'Address Not Added'},status=status.HTTP_400_BAD_REQUEST)


class SelectFarmer(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    
    def get(self,request):
        try:
            farmer_obj = Farmer.objects.filter(district = request.user.district._id)
            serializer = FarmerSerializer(farmer_obj, many=True)
            return Response({'Available Farmers':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':'No Farmers Available At Your District'},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            farmer_obj = Farmer.objects.get(_id=request.data['farmer'])
            if farmer_obj.customer_capacity > 0:
                # customer_obj = Customer.objects.get(_id=request.user._id)
                request.user.farmer = farmer_obj
                request.user.save()
                farmer_obj.customer_capacity -= 1
                farmer_obj.save()
                return Response({'detail':'Farmer is Added To Favourite.'},status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':'OOps Farmer Not Available.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail':'Error While Selecting Farmer Try Again Later'},status=status.HTTP_400_BAD_REQUEST)


class ProductList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    page_size = 1
    page = 1
  
    def get(self,request):     
        try:
            if request.data['search']:
                   
                product_data = Products.objects.filter(name__contains = request.data['search'],farmer___id=request.user.farmer._id)
                if product_data.count() > 0:
                    page = self.paginate_queryset(product_data)
                    if page is not None:
                        serializer = self.get_serializer(page, many=True)
                        return self.get_paginated_response(serializer.data)

                    serializer = self.get_serializer(product_data, many=True)
                    return Response(serializer.data)
                else:
                    return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)

            product_data = Products.objects.filter(farmer___id=request.user.farmer._id)
            if product_data.count() > 0:
                page = self.paginate_queryset(product_data)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(product_data, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            
            return Response({'detail':'Error To Get Product Or Farmer Not Selected'},status=status.HTTP_404_NOT_FOUND)


class ProductDetail(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request,product_id):
        try:
            product_obj = Products.objects.get(_id = product_id)
            serializer = ProductSerializer(product_obj)
            return Response({'detail':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Product Not Found'},status=status.HTTP_204_NO_CONTENT)


class AddProductCart(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request,product_id):
        try:
            cart_obj = Cart.objects.get(user___id=request.user._id)
            serializer = CartFieldSerializer(data=request.data)
            serializer.is_valid()
            product_obj = Products.objects.get(_id=product_id)
          
            if int(serializer.validated_data['qty']) <= product_obj.en.stock:  
                
                if cart_obj.item != None:
                    for item in cart_obj.item:
                        if str(item.product._id) == product_id:
                            return Response({'detail':'Product Already Present'})

                    cartfield_obj = serializer.save(product=product_obj)
                    cart_obj.item.append(cartfield_obj)
                    cart_obj.save()
                    return Response({'detail':'Product Added To Cart'},status=status.HTTP_201_CREATED) 

                cartfield_obj = serializer.save(product=product_obj)
                cart_obj.item = []
                cart_obj.item.append(cartfield_obj)
                cart_obj.save()
                return Response({'detail':'Product Added To Cart'},status=status.HTTP_201_CREATED)   
            
            return Response({'detail':'Sorry Qty Not Available'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
           
            return Response({'detail':serializer.errors},status=status.HTTP_404_NOT_FOUND)
            

class CartList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CartFieldSerializer
    pagination_class = CartPagination
    page_size = 1
    page = 1
    
    def get(self,request):
        try:
            cart_obj = Cart.objects.get(user___id = request.user._id)
            if cart_obj.item != []:
                page = self.paginate_queryset(cart_obj.item)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(cart_obj.item, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail':'Error To Get Product'},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request):
        try:
            cart_obj = Cart.objects.get(user___id=request.user._id)
            for item in cart_obj.item:
                cart_obj.item.remove(item)
                cart_obj.save()          
            return Response({"detail":"Cart Empted"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail':'Error To Delete CartList'},status=status.HTTP_404_NOT_FOUND)
        

class DeleteProductCart(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def delete(self,request,product_id):
        try:
            cart_obj = Cart.objects.get(user___id = request.user._id)
            for item in cart_obj.item:
                if str(item.product._id) == product_id:
                    cart_obj.item.remove(item)
                    cart_obj.save()  
                    return Response({'detail':'Product Removed From Cart'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'Product Already Removed.'},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Product Not Removed From Cart'},status=status.HTTP_400_BAD_REQUEST)


class BuyProduct(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request,product_id):
        try:
            qty_serializer = QtySerializer(data = request.data)
            qty_serializer.is_valid()
            product_obj = Products.objects.get(_id=product_id)
            qty = int(qty_serializer.data['qty'])
            product_serializer = ProductSerializer(product_obj)
            if qty <= product_obj.en.stock:

                resulted_data = {
                        'product': product_serializer.data,
                        'qty': qty,
                        'total': qty*product_obj.en.price
                } 
                return Response({'detail':resulted_data},status=status.HTTP_200_OK)
            return Response({'detail':'Qty Not Available'})
        except Exception as e:
            pass


    def post(self,request,product_id):
        try:
            serializer = QtySerializer(data=request.data)
            if serializer.is_valid():
                product_obj = Products.objects.get(_id = product_id)
                for address in request.user.addresses:
                    if str(address._id) == request.data['address']: 
                        new_address = address
                        break 
                else:
                    return Response({'detail':'Address Not Found '},status=status.HTTP_400_BAD_REQUEST)
                order_field = {'product':product_id,'qty':int(serializer.validated_data['qty'])}
                serializer2 = OrderFieldSerializer(data=order_field)
                serializer2.is_valid()
                order_field_obj = serializer2.save()

                order_dict = {
                        'customer' : request.user,
                        'farmer': request.user.farmer,
                        'items': [order_field_obj,],
                        'address': new_address,
                        'total': int(serializer.validated_data['qty'] * product_obj.en.price),
                        'payment_method': request.data['payment_method']
                }
                order_obj = Order(**order_dict)
                order_obj.save()
                order_serializer = OrderSerializer(order_obj)
                mail_sender_farmer.delay(order_serializer.data['_id'])
                mail_sender_user.delay(request.user.email)
                return Response({'detail':'Ordered Placed Successfully',
                                'data':order_serializer.data
                                },status=status.HTTP_201_CREATED)
                
            return Response({'detail',serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:         
            return Response({'detail':'Ordered Failed To Placed'})


class CartCheckout(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self,request):
        try:
            cart_obj = Cart.objects.get(user___id = request.user._id)
            if cart_obj.item != []: 
                serializer = CartFieldSerializer(cart_obj.item, many=True)
                return Response({'detail':serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"detail":"No Products Found."},status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'detail':'Error To Get Cart Products'},status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request):
        try:
            cart_obj = Cart.objects.get(user___id = request.user._id) 
            total  = 0
            order_field_list = []
        
            for address in request.user.addresses:
                if str(address._id) == request.data['address']: 
                    new_address = address
                    break 
            else:
                return Response({'detail':'Address Not Found '},status=status.HTTP_400_BAD_REQUEST)

            for item in cart_obj.item:
                order_field = {'product':item.product._id,'qty':item.qty}
                serializer2 = OrderFieldSerializer(data=order_field)
                serializer2.is_valid()
                order_field_list.append(serializer2.save())
                total += item.product.en.price


            order_dict = {
                        'customer' : request.user,
                        'farmer' : request.user.farmer,
                        'items': order_field_list,
                        'address': new_address,
                        'total': total,
                        'payment_method': request.data['payment_method']
                }
            order_obj = Order(**order_dict)
            order_obj.save()
            order_serializer = OrderSerializer(order_obj)
            mail_sender_farmer.delay(order_serializer.data['_id'])
            mail_sender_user.delay(request.user.email)
            return Response({'detail':'Ordered Placed Successfully',
                            'data':order_serializer.data
                            },status=status.HTTP_201_CREATED)     
        except Exception as e:
            return Response({'detail':'Ordered Failed To Placed'})

class OrderList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    page_size = 1
    page = 1
    
    def get(self,request):
        try:
            order_obj = Order.objects.filter(customer___id=request.user._id)    
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

    def get(self,request,order_id):
        try:
            order_obj = Order.objects.get(_id=order_id)
            serializer = OrderSerializer(order_obj)
            return Response({'detail':serializer.data},status=status.HTTP_200_OK)          
        except:
            return Response({'detail':'Error TO Get Order Detail'},status=status.HTTP_404_NOT_FOUND)

class ChangeFarmer(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        try:
            farmer_obj1 = Farmer.objects.get(_id=request.user.farmer._id)
            farmer_obj1.customer_capacity += 1
            farmer_obj1.save()
            cart_obj = Cart.objects.get(user___id=request.user._id)
            for item in cart_obj.item:
                cart_obj.item.remove(item)
                cart_obj.save()        

            farmer_obj2 = Farmer.objects.get(_id=request.data['farmer'])
            if farmer_obj2.customer_capacity > 0:
                request.user.farmer = farmer_obj2
                request.user.save()
                farmer_obj2.customer_capacity -= 1
                farmer_obj2.save()
                return Response({'detail':'Farmer is Added To Favourite.'},status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':'OOps Farmer Not Available.'},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail':'Error While Changing Farmer Try Again Later'},status=status.HTTP_400_BAD_REQUEST)