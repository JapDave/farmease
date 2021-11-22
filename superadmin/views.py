from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login
from .forms import CategoryForm, DistrictForm, LoginForm, StateForm
from subadmin.models import SubAdmin
from customer.models import  Customer
from farmer.models import Categories, Farmer,State,District
from django.core.paginator import Paginator
from .forms import AdminForm



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
      return render(request,'index.html')


class AddState(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = StateForm
      return render(request,'add_state.html',{'form':form})

   def post(self,request):
      form = StateForm(request.POST)
      if form.is_valid():
         form.save()
         return render(request,'add_state.html',{'form':form,'msg':'State Added'})
      else:
         return render(request,'add_state.html',{'form':form,'msg':'State Not Added'})

class StateView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         state_obj = State.objects.all()
         if state_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(state_obj,10)
            state_data = paginator.page(page)
            return render(request,'show_state.html',{'results':state_data})
         else:
            return render(request,'show_state.html',{'msg':'No State Add Yet'})
      except:
         pass
         #404

class AddDistrict(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = DistrictForm
      return render(request,'add_district.html',{'form':form})

   def post(self,request):
      form = DistrictForm(request.POST)
      if form.is_valid():
         form.save()
         return render(request,'add_state.html',{'form':form,'msg':'District Added'})
      else:
         return render(request,'add_state.html',{'form':form,'msg':'District Not Added'})


class DistrictView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         district_obj = District.objects.all()
         if district_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(district_obj,10)
            district_data = paginator.page(page)
            return render(request,'show_district.html',{'results':district_data})
         else:
            return render(request,'show_district.html',{'msg':'No State Add Yet'})
      except:
         pass
         #404

class AddCategory(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = CategoryForm
      return render(request,'add_category.html',{'form':form})

   def post(self,request):
      form = CategoryForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         return render(request,'add_category.html',{'form':form,'msg':'Category Added'})
      else:
         return render(request,'add_category.html',{'form':form,'msg':'Category Not Added'})


class CategoryView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         category_obj = Categories.objects.all()
         if category_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(category_obj,10)
            category_data = paginator.page(page)
            return render(request,'show_category.html',{'results':category_data})
         else:
            return render(request,'show_category.html',{'msg':'No State Add Yet'})
      except:
         pass
         #404


class AddAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = AdminForm
      return render(request,'add_admin.html',{'form':form})

   def post(self,request):
      form  = AdminForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         return render(request,'add_admin.html',{'form':form,'msg':'New Admin Added'})
      else:
         return render(request,'add_admin.html',{'form':form,'msg':'Error To Add Admin'})
 
class Admin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      try:
         admin_obj = SubAdmin.objects.all()
         if admin_obj:
            page = request.GET.get('page',1)
            paginator = Paginator(admin_obj,10)
            admin_data = paginator.page(page)
            return render(request,'show_admin.html',{'results':admin_data})
         else:
            return render(request,'show_admin.html',{'msg':'No Admins Add Yet'})
      except:
         pass