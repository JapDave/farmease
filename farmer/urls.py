from django.urls import path,include
from .views import *


urlpatterns = [
   path('getmaster',GetMaster.as_view()),
   path('register',Register.as_view()),
   path('login',Login.as_view()),
   path('logout',Logout.as_view()),
   path('profile',Profile.as_view()),
   path('addproduct',AddProduct.as_view()),
   path('allproducts',AllProducts.as_view()),
   path('productdetail/<id>',ProductDetail.as_view()),
   path('customers',CustomerList.as_view())

]
