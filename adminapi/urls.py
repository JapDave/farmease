from django.urls import path,include
from .views import *
from farmer.views import Register
from customer.views import  Register as customer_reg

urlpatterns = [
   path('forgotpassword',ForgotPassword.as_view()),
   path('otpverification',OtpVerification.as_view()),
   path('changepassword',ChangePassword.as_view()),
   path('login', Login.as_view()),
   path('logout', Logout.as_view()),
   path('profile', Profile.as_view()),
   path('profilechangepassword/<admin_id>', ProfileChangePassword.as_view()),
   path('addfarmer', FarmerRegister.as_view()),
   path('farmers', FarmerList.as_view()),
   path('addcustomer', customer_reg.as_view()),
   path('customers', CustomerList.as_view()),
   path('farmerdetail/<farmer_id>', FarmerDetail.as_view()),
   path('customerdetail/<customer_id>', CustomerDetail.as_view()),
   path('products', ProductList.as_view()),
   path('addproduct', AddProduct.as_view()),
   path('productdetail/<product_id>', ProductDetail.as_view()),
   path('orderhistory/<farmer_id>', OrderHistory.as_view()),
   path('orderdetail/<order_id>', OrderDetail.as_view()),
  
]
