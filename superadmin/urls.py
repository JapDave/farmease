from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.utils.translation import ugettext_lazy as _



urlpatterns = [
   path('login',Login.as_view(),name='login'),
   path('logout',Logout.as_view(),name='logout'),
   path('',Index.as_view(),name='index'), 

   path('addstate',AddState.as_view(),name='addstate'),
   path('states',StateView.as_view(),name='allstate'),
   path('deletestate/<id>',DeleteState.as_view(),name='deletestate'),
   path('updatestate/<id>',UpdateState.as_view(),name='updatestate'),
   
   path('adddistrict',AddDistrict.as_view(),name='adddistrict'),
   path('districts',DistrictView.as_view(),name='alldistrict'),
   path('deletedistrict/<id>',DeleteDistrict.as_view(),name='deletedistrict'),
   path('updatedistrict/<id>',UpdateDistrict.as_view(),name='updatedistrict'),
   
   
   # Category Section 
   path('addcategory',AddCategory.as_view(),name='addcategory'),
   path('categories',CategoryView.as_view(),name='allcategory'),
   path('deletecategory/<id>',DeleteCategory.as_view(),name='deletecategory'),
   path('updatecategory/<id>',UpdateCategory.as_view(),name='updatecategory'),

   # Admin Section
   path('addadmins',AddAdmin.as_view(),name='addadmin'),
   path('admins',AdminView.as_view(),name='alladmin'),
   path('deleteadmin/<id>',DeleteAdmin.as_view(),name='deleteadmin'),
   path('updateadmin/<id>',UpdateAdmin.as_view(),name='updateadmin'),
   path('detailadmin/<id>',DetailAdmin.as_view(),name='detailadmin'),

   # Farmer Section
   path('addfarmer',AddFarmer.as_view(),name='addfarmer'),
   path('farmers',FarmerView.as_view(),name='allfarmer'),
   path('deletefarmer/<id>',DeleteFarmer.as_view(),name='deletefarmer'),
   path('updatefarmer/<id>',UpdateFarmer.as_view(),name='updatefarmer'),
   path('detailfarmer/<id>',DetailFarmer.as_view(),name='detailfarmer'),


   # Customer Section
   path('addcustomer',AddCustomer.as_view(),name='addcustomer'),
   path('customers',CustomerView.as_view(),name='allcustomer'),
   path('deletecustomer/<id>',DeleteCustomer.as_view(),name='deletecustomer'),
   path('updatecustomer/<id>',UpdateCustomer.as_view(),name='updatecustomer'),
   path('detailcustomer/<id>',DetailCustomer.as_view(),name='detailcustomer'),
   path('addaddress/<customer_id>',AddAddress.as_view(),name='addaddress'),
   path('addresses/<id>',AddressView.as_view(),name='alladdress'),
   path('updateaddress/<customer_id>/<id>',UpdateAddress.as_view(),name='updateaddress'),
   path('deletaddress/<customer_id>/<id>',DeleteAddress.as_view(),name='deleteaddress'),
   
   # Product Section
   path('addproduct',AddProduct.as_view(),name='addproduct'),
   path('products',ProductView.as_view(),name='allproduct'),
   path('deleteproduct/<id>',DeleteProduct.as_view(),name='deleteproduct'),
   path('updateproduct/<id>',UpdateProduct.as_view(),name='updateproduct'),
   path('detailproduct/<id>',DetailProduct.as_view(),name='detailproduct'),
   
   # Order Section
   path('addorder',AddOrder.as_view(),name='addorder'),
   path('orders',OrderView.as_view(),name='allorder'),
   path('deleteorder/<id>',DeleteOrder.as_view(),name='deleteorder'),
   path('updateorder/<id>',UpdateOrder.as_view(),name='updateorder'),
   path('detailorder/<id>',DetailOrder.as_view(),name='detailorder'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)