from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, CustomerSerializer,TokenSerializer,LoginUserSerializer
from .models import Customer, Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_auth.views import LoginView as RestLoginView
from rest_framework.views import APIView
from .authentication import TokenAuthentication
# from .paginations import ProductPagination


class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CustomerSerializer(user,context=self.get_serializer_context()).data,
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
   serializer_class = CustomerSerializer

   def get(self, request):
        profile = Customer.objects.get(_id=request.user._id)         
        serializer = CustomerSerializer(profile)
        return Response(serializer.data)

   def post(self, request):       
        serializer = CustomerSerializer(Customer.objects.get(_id=request.user._id),data=request.data)
        if serializer.is_valid():
            serializer.update(Customer.objects.get(_id=request.user._id),request.data)
            return Response({'detail':'Profile Updated'},status=status.HTTP_201_CREATED)
        else:
            return Response({'detail':serializer.errors},status=status.HTTP_400_BAD_REQUEST)