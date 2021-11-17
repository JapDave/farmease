from django.urls import path,include
from .views import *


urlpatterns = [
   path('getmaster',GetMaster.as_view()),
   path('register',Register.as_view()),
   path('login',Login.as_view()),
   path('logout',Logout.as_view()),
   path('profile',Profile.as_view()),
   path('address',AddressView.as_view()),
   path('addaddress',AddAddress.as_view()),
   path('addressdetail/<address_id>',AddressDetail.as_view()),
   path('farmers',SelectFarmer.as_view()),
   path('changefarmer',ChangeFarmer.as_view()),
   path('products',ProductList.as_view()),
   path('productdetail/<product_id>',ProductDetail.as_view()),
   path('addproductcart/<product_id>',AddProductCart.as_view()),
   path('deleteproductcart/<product_id>',DeleteProductCart.as_view()),
   path('buyproduct/<product_id>',BuyProduct.as_view()),
   path('cart',CartList.as_view()),
   path('checkout',CartCheckout.as_view()),
   path('orders',OrderList.as_view()),
   path('orderdetail/<order_id>',OrderDetail.as_view()),
   
]
