from django.urls import path,include
from .views import *


urlpatterns = [
   path('getmaster',GetMaster.as_view()),
   path('register',Register.as_view()),
   path('login',Login.as_view()),
   path('logout',Logout.as_view()),
   path('profile',Profile.as_view()),
   path('address/<customer_id>',AddressView.as_view()),
   path('addaddress/<customer_id>',AddAddress.as_view()),
   path('addressdetail/<address_id>',AddressDetail.as_view()),
   path('farmers',SelectedFarmerView.as_view()),
   path('products',ProductList.as_view()),
   path('productdetail/<product_id>',ProductDetail.as_view()),
   path('productcart/<product_id>',ProductCartView.as_view()),
   path('cart',CartList.as_view()),
   
]
