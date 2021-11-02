from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ProductSerializer, RegisterSerializer, FarmerSerializer,LoginUserSerializer,TokenSerializer,AddProductSerializer
from .models import Categories, Farmer, Products, Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_auth.views import LoginView as RestLoginView
from rest_framework.views import APIView
from .authentication import TokenAuthentication
from .paginations import ProductPagination


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
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": FarmerSerializer(user,context=self.get_serializer_context()).data,
            "message": "Farmer Created Successfully.  Now perform Login to get your token",
        })


class Logout(APIView):

    # permission_classes = (IsAuthenticated,)
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

    def get(self, request):
        profile = Farmer.objects.get(_id=request.user._id)         
        serializer = FarmerSerializer(profile)
        return Response(serializer.data)

    def post(self, request):       
        serializer = FarmerSerializer(Farmer.objects.get(_id=request.user._id),data=request.data)      
        if serializer.is_valid():
           serializer.update(Farmer.objects.get(_id=request.user._id),request.data)
           return Response({'detail':'Profile Updated'},status=status.HTTP_201_CREATED)
        else:
           return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
       


class AddProduct(generics.GenericAPIView):
    def post(self,request):
        try:
            request.data['farmer']= request.user._id
            serializer = AddProductSerializer(data=request.data)
            serializer.is_valid()                  
            serializer.save()
            return Response({'detail':'Product Added'},status=status.HTTP_201_CREATED)
        except:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)



class AllProducts(generics.GenericAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    page_size = 1
    page = 1
  
    def get(self,request):     
        serializer = ProductSerializer(Products.objects.filter(farmer___id=request.user._id), many=True)
        if serializer.data:
            page = self.paginate_queryset(Products.objects.filter(farmer___id=request.user._id))
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(Products.objects.filter(farmer___id=request.user._id), many=True)
            return Response(serializer.data)

        else:
            return Response({"detail":"No Products Found."},status=status.HTTP_200_OK)
    
       
class ProductDetail(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self,request,id):
        try:
            serializer = ProductSerializer(Products.objects.get(_id=id))
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Product Not Found'},status=status.HTTP_204_NO_CONTENT)


    def post(self,request,id):
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid()       
            serializer.update(Products.objects.get(_id=id),request.data)
            return Response({'detail':'Product Updated'},status=status.HTTP_201_CREATED)
        except:
            return Response({'detail':'Product Not Updated'},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        try:
            Products.objects.get(_id=id).delete()
            return Response({'detail':'Product Deleted'},status=status.HTTP_200_OK)
        except:
            return Response({'detail':'Error While Deleting'},status=status.HTTP_400_BAD_REQUEST)