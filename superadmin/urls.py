from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('login',Login.as_view(),name='login'),
   path('',Index.as_view(),name='index')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


