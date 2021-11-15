from farmer.models import Farmer,Products
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import AddressSerializer, CartSerializer, RegisterSerializer, CustomerSerializer,TokenSerializer,LoginUserSerializer,CartFieldSerializer
from farmer.serializers import CategorySerializer,StateSerializer,DistrictSerializer,FarmerSerializer,ProductSerializer
from .models import Cart, Customer, Token, State, District,Categories
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_auth.views import LoginView as RestLoginView
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from farmer.paginations import ProductPagination

class GetMaster(generics.GenericAPIView):
    def get(self,request):
        category_serial = CategorySerializer(Categories.objects.all(), many=True)
        state_serial = StateSerializer(State.objects.all(), many=True)
        district_serial = DistrictSerializer(District.objects.all(), many=True)
        return Response({'result':{'categories':category_serial.data,
                                    'states':state_serial.data,
                                    'district':district_serial.data}},status=status.HTTP_200_OK)


class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)     
        serializer.is_valid(raise_exception=True)      
        serializer.save()
        return Response({
            "user": serializer.data,
            "message": "Customer Created Successfully.  Now perform Login to get your token",
        })

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
        profile = Customer.objects.get(_id=request.user._id)         
        serializer = CustomerSerializer(profile)
        return Response(serializer.data)

   def post(self, request):       
        serializer = CustomerSerializer(Customer.objects.get(_id=request.user._id),data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Profile Updated'},status=status.HTTP_201_CREATED)
        else:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class AddressView(generics.GenericAPIView):
        authentication_classes = (TokenAuthentication,)

        def get(self,request,customer_id):
            try:
                customer_obj = Customer.objects.get(_id=customer_id)
                serializer = AddressSerializer(customer_obj.addresses,many=True)
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
    
    def post(self,request,customer_id):
        try:
            customer_obj = Customer.objects.get(_id=customer_id)
            address_serializer = AddressSerializer(data=request.data)
            if address_serializer.is_valid():              
                address_obj = address_serializer.save()
                customer_obj.addresses.append(address_obj)
                customer_obj.save()
                return Response({'detail':'Address Added Successfully',
                                'address':address_serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response({'detail':address_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'detail':'Address Not Added'},status=status.HTTP_400_BAD_REQUEST)


class SelectedFarmerView(generics.GenericAPIView):
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
                customer_obj = Customer.objects.get(_id=request.user._id)
                customer_obj.farmer = farmer_obj
                customer_obj.save()
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


class ProductCartView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self,request,product_id):
        try:
            cart_obj = Cart.objects.get(user___id=request.user._id)
            serializer = CartFieldSerializer(data=request.data)
            serializer.is_valid()
            if cart_obj.item != None:
                for item in cart_obj.item:
                    if str(item.product._id) == product_id:
                        return Response({'detail':'Product Already Present'})

                cartfield_obj = serializer.save(product=Products.objects.get(_id=product_id))
                cart_obj.item.append(cartfield_obj)
                cart_obj.save()
                return Response({'detail':'Product Added To Cart'},status=status.HTTP_201_CREATED) 

            cartfield_obj = serializer.save(product=Products.objects.get(_id=product_id))
            cart_obj.item = []
            cart_obj.item.append(cartfield_obj)
            cart_obj.save()
            return Response({'detail':'Product Added To Cart'},status=status.HTTP_201_CREATED)      
        except Exception as e:
            return Response({'detail':serializer.errors},status=status.HTTP_404_NOT_FOUND)
            

class CartList(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = CartFieldSerializer
    pagination_class = ProductPagination
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
            print(e)
            return Response({'detail':'Error To Delete CartList'},status=status.HTTP_404_NOT_FOUND)
        