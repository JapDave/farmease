from django.urls import path,include
from .views import *
from farmer.views import Register
from customer.views import  Register as customer_reg

urlpatterns = [
   # path('forgotpassword',ForgotPassword.as_view()),
   # path('otpverification',OtpVerification.as_view()),
   # path('changepassword',ChangePassword.as_view()),
     path('login', Login.as_view(),name='login'),
     path('index', Index.as_view(),name='admin_index'),
     path('farmers', AllFarmer.as_view(),name='admin_allfarmer'),
  
  
]
