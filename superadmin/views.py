from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login
from .forms import AddressForm, CategoryForm, DistrictForm, LoginForm, OrderFieldForm, OrderForm, StateForm
from subadmin.models import SubAdmin
from customer.models import  Customer, Order, OrderField
from farmer.models import Categories, Farmer, Products,State,District
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from .forms import AdminForm,FarmerForm,CustomerForm,ProductForm
from django.utils import translation

def language(request):
   if request.GET.get('prefered_language'):
      # translation.activate(request.GET.get('prefered_language'))
      request.session['language'] = request.GET.get('prefered_language')
   translation.activate(request.session['language'])

class Login(View):

   def get(self,request):
      form = LoginForm
      return render(request,'login.html',{'form':form})

   def post(self,request):
      form = LoginForm(request.POST)
      if form.is_valid():
         username = form.cleaned_data.get("username")
         password = form.cleaned_data.get("password")
         user = authenticate(username=username, password=password)
         if user is not None:
               login(request, user)
               return redirect(reverse('index'))
         else:            
            return render(request,'login.html',{'form':form,'msg':'Invalid Credientials'})
      else:
         return render(request,'login.html',{'form':form})


class Index(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      # request.session[settings.LANGUAGE_SESSION_KEY] = 'en'
      if request.GET.get('prefered_language'):
         language(request)
         return render(request,'index.html',{'lan':request.session['language']})
      return render(request,'index.html')


class AddState(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = StateForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_state.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         form = StateForm(request.POST)
         language(request)
         lan = request.session['language']

         if lan == 'gu':
            msg = 'રાજ્ય ઉમેર્યું'
         else:
            msg = 'State Added'   
         form.is_valid()
         form.save()
         return render(request,'add_state.html',{'form':form,'msg':msg,'lan':lan})
      except:
            if lan == 'gu':
               msg = 'રાજ્ય નથી ઉમેર્યું'
            else:
               msg = 'State Not Added'  
            return render(request,'add_state.html',{'form':form,'msg':msg,'lan':lan})

class StateView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         state_obj = State.objects.all()
         language(request)
         lan = request.session['language']
         
         if state_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(state_obj,10)
            state_data = paginator.page(page)
            return render(request,'show_state.html',{'results':state_data,'lan':lan})
         else:
            if lan == 'gu':
               msg = 'હજુ સુધી કોઈ રાજ્ય ઉમેર્યું નથી'
            else:
               msg = 'No State Added Yet'
            return render(request,'show_state.html',{'msg': msg,'lan':lan })
      except:
         pass
         #404

class AddDistrict(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = DistrictForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_district.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         form = DistrictForm(request.POST)
         language(request)
         lan = request.session['language']
         if lan == 'gu':
            msg = 'જિલ્લો ઉમેર્યું'
         else:
            msg = 'District Added'   

         form.is_valid()
         form.save()
        
         return render(request,'add_state.html',{'form':form,'msg':msg,'lan':lan})
      except:
         if lan == 'gu':
               msg = 'જિલ્લો નથી ઉમેર્યું'
         else:
            msg = 'District Not Added'   

         return render(request,'add_state.html',{'form':form,'msg': msg,'lan':lan})

class DistrictView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         district_obj = District.objects.all()
         language(request)
         lan = request.session['language']
         
         if district_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(district_obj,10)
            district_data = paginator.page(page)
           
            return render(request,'show_district.html',{'results':district_data,'lan':lan})
         else:
            if lan == 'gu':
               msg = 'હજુ સુધી કોઈ જિલ્લો ઉમેર્યું નથી'
            else: 
               msg = 'District Not Added yet'   
            return render(request,'show_district.html',{'msg': msg,'lan':lan})
      except:
         pass
         #404

class AddCategory(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = CategoryForm()     
      language(request)
      lan = request.session['language']

      return render(request,'add_category.html',{'form':form,'lan':lan})

   def post(self,request):
      form = CategoryForm(request.POST,request.FILES)
      try:
         language(request)
         lan = request.session['language']

         if lan == 'gu':
            msg = 'શ્રેણીઓ ઉમેર્યું'
         else:
            msg = 'Category Added'   

         form.is_valid()
         form.save()
         return render(request,'add_category.html',{'form':form,'msg':msg,'lan':lan})
      except:
         if lan == 'gu':
            msg = 'શ્રેણીઓ નથી ઉમેર્યું'
         else:
            msg = 'Category Not Added'   
         return render(request,'add_category.html',{'form':form,'msg':msg,'lan':lan})

class CategoryView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         category_obj = Categories.objects.all()
         language(request)
         lan = request.session['language']

         if category_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(category_obj,10)
            category_data = paginator.page(page)
            return render(request,'show_category.html',{'results':category_data,'lan':lan})
         else:
            if lan == 'gu':
               msg = 'હજુ સુધી કોઈ શ્રેણી ઉમેરાઈ નથી'
            else:
               msg = 'No Category Added Yet'
            return render(request,'show_category.html',{'lan':lan,'msg':msg})
      except Exception as e:
         print(e)
         pass
         #404


class AddAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = AdminForm()
      language(request)
      lan = request.session['language']


      return render(request,'add_admin.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         language(request)
         lan = request.session['language']

         if lan == 'gu':
            msg = 'નવો એડમિન ઉમેરાયો'
         else:
            msg = 'New Admin Added' 
         form  = AdminForm(request.POST,request.FILES)
         form.is_valid()
         form.save()
         return render(request,'add_admin.html',{'form':form,'msg': msg,'lan':lan})
      except:
         if lan == 'gu':
               msg = 'એડમિન નથી ઉમેરાયો'
         else:
            msg = 'Admin Not Added'   
         return render(request,'add_admin.html',{'form':form,'msg': msg,'lan':lan})
 
class AdminView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         admin_obj = SubAdmin.objects.all()
         language(request)
         lan = request.session['language']

         if admin_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(admin_obj,10)
            admin_data = paginator.page(page)
            return render(request,'show_admin.html',{'results':admin_data,'lan':lan})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ એડમિન ઉમેરાઈ નથી'
            else:
               msg = 'No Admin Added Yet'
            return render(request,'show_admin.html',{'msg': msg,'lan':lan})
      except:
         pass

class AddFarmer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = FarmerForm()
      language(request)
      lan = request.session['language']      

      return render(request,'add_farmer.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         language(request)
         lan = request.session['language']
         
         if lan == 'gu':
            msg = 'નવો ખેડૂત ઉમેરાયો'
         else:
            msg = 'New Farmer Added' 
         form  = FarmerForm(request.POST,request.FILES)
         form.is_valid()
         form.save()
         return render(request,'add_farmer.html',{'form':form,'msg': msg,'lan':lan})
      except:
         if lan == 'gu':
               msg = 'ખેડૂત નથી ઉમેરાયો'
         else:
            msg = 'Farmer Not Added'   
         return render(request,'add_farmer.html',{'form':form,'msg': msg,'lan':lan})
 
class FarmerView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         farmer_obj = Farmer.objects.all()
         language(request)
         lan = request.session['language'] 
        
         if farmer_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(farmer_obj,10)
            farmer_data = paginator.page(page)
            return render(request,'show_farmer.html',{'results':farmer_data,'lan':lan})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ખેડૂત ઉમેરાઈ નથી'
            else:
               msg = 'No Farmer Added Yet'
            return render(request,'show_farmer.html',{'msg': msg,'lan':lan})
      except:
         pass


class AddCustomer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = CustomerForm()
      addressform = AddressForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_customer.html',{'form':form,'addressform':addressform,'lan':lan})

   def post(self,request):
      try:
         language(request)
         lan = request.session['language']
         if lan == 'gu':
            msg = 'નવો ગ્રાહક ઉમેરાયો'
         else:
            msg = 'New Customer Added' 
         form  = CustomerForm(request.POST,request.FILES)
         addressform = AddressForm(request.POST,request.FILES)
        
         if addressform.is_valid():
           
            address_obj = addressform.save(commit=False)    
            customer_obj = form.save(commit=False)
            customer_obj.addresses = [address_obj,]
            customer_obj.save()

         return render(request,'add_customer.html',{'form':form,'addressform':addressform, 'msg': msg,'lan':lan})
      except Exception as e:
         if lan == 'gu':
               msg = 'ગ્રાહક નથી ઉમેરાયો'
         else:
            msg = 'Customer Not Added'   
         return render(request,'add_customer.html',{'form':form,'addressform':addressform,'msg': msg,'lan':lan})
 
class CustomerView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         customer_obj = Customer.objects.all()
         language(request)
         lan = request.session['language']
         
         if customer_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(customer_obj,10)
            customer_data = paginator.page(page)
            return render(request,'show_customer.html',{'results':customer_data,'lan':lan})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ગ્રાહક ઉમેરાઈ નથી'
            else:
               msg = 'No Customer Added Yet'
            return render(request,'show_customer.html',{'msg': msg,'lan':lan})
      except:
         pass


class AddProduct(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = ProductForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_product.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         language(request)
         lan = request.session['language']
         
         if lan == 'gu':
            msg = 'નવો ઉત્પાદનો ઉમેરાયો'
         else:
            msg = 'New Product Added' 
         form  = ProductForm(request.POST,request.FILES)
         form.is_valid()
         form.save()
         return render(request,'add_product.html',{'form':form,'msg': msg,'lan':lan})
      except:
         if lan == 'gu':
               msg = 'ઉત્પાદનો નથી ઉમેરાયો'
         else:
            msg = 'Product Not Added'   
         return render(request,'add_product.html',{'form':form,'msg': msg,'lan':lan})
 
class ProductView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         product_obj = Products.objects.all()
         language(request)
         lan = request.session['language']
         
         if product_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(product_obj,10)
            product_data = paginator.page(page)
            return render(request,'show_product.html',{'results':product_data,'lan':lan})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ઉત્પાદનો ઉમેરાઈ નથી'
            else:
               msg = 'No Product Added Yet'
            return render(request,'show_product.html',{'msg': msg,'lan':lan})
      except:
         pass  



class AddOrder(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = OrderForm()
      orderfieldform = OrderFieldForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_order.html',{'form':form,'itemform':orderfieldform,'lan':lan})

   def post(self,request):
      try:
         language(request)
         lan = request.session['language']
         
         if lan == 'gu':
            msg = 'નવો ઓર્ડર ઉમેરાયો'
         else:
            msg = 'New Order Added' 
         form  = OrderForm(request.POST,request.FILES)
         orderfieldform = OrderFieldForm(request.POST,request.FILES)
        
         if orderfieldform.is_valid():
           
            orderfield_obj = orderfieldform.save(commit=False)   
            order_obj = form.save(commit=False)
            print(order_obj)
            order_obj.items = [orderfield_obj,]
            order_obj.save()
           
         
         return render(request,'add_order.html',{'form':form,'itemform':orderfieldform,'msg': msg,'lan':lan})
      except Exception as e:
         print(e)
         if lan == 'gu':
               msg = 'ઓર્ડર નથી ઉમેરાયો'
         else:
            msg = 'Order Not Added'   
         return render(request,'add_order.html',{'form':form,'itemform':orderfieldform,'msg': msg,'lan':lan})
 
class OrderView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         order_obj = Order.objects.all()
         language(request)
         lan = request.session['language']
         
         if order_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(order_obj,10)
            order_data = paginator.page(page)
            return render(request,'show_order.html',{'results':order_data,'lan':lan})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ઓર્ડર ઉમેરાઈ નથી'
            else:
               msg = 'No Orders Added Yet'
            return render(request,'show_order.html',{'msg': msg,'lan':lan})
      except:
         pass  