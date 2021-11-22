from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login
from .forms import AddressForm, CategoryForm, DistrictForm, LoginForm, StateForm
from subadmin.models import SubAdmin
from customer.models import  Customer
from farmer.models import Categories, Farmer,State,District
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from .forms import AdminForm,FarmerForm,CustomerForm


def language(request):
   if request.session['lan']:
         lan = request.session['lan']
   if request.GET.get('prefered_language'):
      lan = request.GET.get('prefered_language')
      request.session['lan'] = lan
   return lan


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
      if request.GET.get('prefered_language'):
         lan = request.GET['prefered_language']
         request.session['lan'] = lan
         return render(request,'index.html',{'lan':lan})
      return render(request,'index.html')


class AddState(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = StateForm()
      lan = language(request)
      return render(request,'add_state.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         form = StateForm(request.POST)
         lan = language(request)

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
         lan = language(request)

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
      lan = language(request)
      return render(request,'add_district.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         form = DistrictForm(request.POST)
         lan = language(request)
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
         lan = language(request)
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
      lan = language(request)

      return render(request,'add_category.html',{'form':form,'lan':lan})

   def post(self,request):
      form = CategoryForm(request.POST,request.FILES)
      try:
         lan = language(request)

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
         lan = language(request)

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
      except:
         pass
         #404


class AddAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = AdminForm()
      lan = language(request)

      return render(request,'add_admin.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         lan = language(request)
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
         lan = language(request)

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
      lan = language(request)

      return render(request,'add_farmer.html',{'form':form,'lan':lan})

   def post(self,request):
      try:
         lan = language(request)
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
         lan = language(request)
         
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
      lan = language(request)
      return render(request,'add_customer.html',{'form':form,'addressform':addressform,'lan':lan})

   def post(self,request):
      try:
         lan = language(request)
         if lan == 'gu':
            msg = 'નવો ગ્રાહક ઉમેરાયો'
         else:
            msg = 'New Customer Added' 
         form  = CustomerForm(request.POST,request.FILES)
         addressform = AddressForm(request.POST,request.FILES)
         if addressform.is_valid():
           
            address_obj = addressform.save(commit=False)
            print('yes')
            form.data._mutable = True
            form.data['addresses'] = [address_obj,]
            form.data._mutable = False	
            # form.is_valid()
            print(form.errors)
            form.save()
       
         return render(request,'add_customer.html',{'form':form,'addressform':addressform, 'msg': msg,'lan':lan})
      except Exception as e:
         print(e)
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
         lan = language(request)
         
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