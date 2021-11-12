from django.urls import path,include
from .views import *


urlpatterns = [
   path('getmaster',GetMaster.as_view()),
   path('register',Register.as_view()),
   path('login',Login.as_view()),
   path('logout',Logout.as_view()),
   path('profile',Profile.as_view()),
]
