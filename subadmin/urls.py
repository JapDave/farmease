from django.urls import path,include
from .views import *


urlpatterns = [
   path('forgotpassword',ForgotPassword.as_view()),
   path('otpverification',OtpVerification.as_view()),
   path('changepassword',ChangePassword.as_view()),
   path('login', Login.as_view()),
   path('profile', Profile.as_view()),
   path('profilechangepassword/<admin_id>', ProfileChangePassword.as_view()),
   path('farmers', FarmerList.as_view()),
   path('farmerdetail/<farmer_id>', FarmerDetail.as_view()),
   path('products/<farmer_id>', ProductList.as_view()),
   path('productdetail/<product_id>', ProductDetail.as_view()),
   path('orderhistory/<farmer_id>', OrderHistory.as_view()),
  

]
