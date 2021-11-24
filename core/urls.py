from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

from django.conf.urls.i18n import i18n_patterns



urlpatterns = [ 
    path('superadmin/', include('superadmin.urls')),
    path('farmerapi/',include('farmer.urls')),
    path('customerapi/',include('customer.urls')),
    path('adminapi/',include('adminapi.urls')),
    path('admin/',include('subadmin.urls')),
   
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(
  
# )
