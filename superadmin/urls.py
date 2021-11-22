from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url




urlpatterns = [
   path('login',Login.as_view(),name='login'),
   path('',Index.as_view(),name='index'),
   path('addadmin',AddAdmin.as_view(),name='addadmin'),
   path('admins',Admin.as_view(),name='alladmin'),
   path('addstate',AddState.as_view(),name='addstate'),
   path('states',StateView.as_view(),name='allstate'),
   path('adddistrict',AddDistrict.as_view(),name='adddistrict'),
   path('districts',DistrictView.as_view(),name='alldistrict'),
   path('addcategory',AddCategory.as_view(),name='addcategory'),
   path('categories',CategoryView.as_view(),name='allcategory'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)