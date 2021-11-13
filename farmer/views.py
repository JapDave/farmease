from customer.serializers import CustomerSerializer
from rest_framework import generics, permissions
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_auth.views import LoginView as RestLoginView
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from .paginations import ProductPagination,CustomerPagination
from customer.models import Customer

class GetMaster(generics.GenericAPIView):
    def get(self,request):
        category_serial = CategorySerializer(Categories.objects.all(), many=True)
        state_serial = StateSerializer(State.objects.all(), many=True)
        district_serial = DistrictSerializer(District.objects.all(), many=True)
        return Response({'result':{'categories':category_serial.data,
                                    'states':state_serial.data,
                                    'district':district_serial.data}},status=status.HTTP_200_OK)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        return Response({
            "user": FarmerSerializer(user,context=self.get_serializer_context()).data,
            "message": "Farmer Created Successfully.  Now perform Login to get your token",
        })


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
            serializer.update(instance,request.data)
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