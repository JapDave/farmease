from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   # path('forgotpassword',ForgotPassword.as_view()),
   # path('otpverification',OtpVerification.as_view()),
   # path('changepassword',ChangePassword.as_view()),
    path('categories',CategoryView.as_view(),name='admin_allcategory'),
    path('state',StateView.as_view(),name='admin_allstate'),
    path('district',DistrictView.as_view(),name='admin_alldistrict'),
    path('login', Login.as_view(),name='admin_login'),
    path('logout', Logout.as_view(),name='admin_logout'),
    path('index', Index.as_view(),name='admin_index'),
    path('addfarmer',AddFarmer.as_view(),name='admin_addfarmer'),
    path('farmers', FarmerView.as_view(),name='admin_allfarmer'),
    path('updatefarmer/<id>',UpdateFarmer.as_view(),name='admin_updatefarmer'),
    path('farmerdetail/<id>',DetailFarmer.as_view(),name='admin_detailfarmer'),
    path('deletefarmer/<id>',DeleteFarmer.as_view(),name='admin_deletefarmer'),
    path('customers', CustomerView.as_view(),name='admin_allcustomer'),
    path('addcustomer', AddCustomer.as_view(),name='admin_addcustomer'),
    path('updatecustomer/<id>',UpdateCustomer.as_view(),name='admin_updatecustomer'),
    path('customerdetail/<id>',DetailCustomer.as_view(),name='admin_detailcustomer'),
    path('deletecustomer/<id>',DeleteCustomer.as_view(),name='admin_deletecustomer'),
    path('products',ProductView.as_view(),name='admin_allproduct'),
    path('addproduct',AddProduct.as_view(),name='admin_addproduct'),
    path('productdetail/<id>',DetailProduct.as_view(),name='admin_detailproduct'),
    path('productdelete/<id>',DeleteProduct.as_view(),name='admin_deleteproduct'),
    path('order',OrderView.as_view(),name='admin_allorder'),
    path('orderdetail/<id>',OrderDetail.as_view(),name='admin_detailorder'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
