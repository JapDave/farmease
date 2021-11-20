from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login
from .forms import LoginForm

class Login(View):

   def get(self,request):
      form = LoginForm
      return render(request,'superadmin/login.html',{'form':form})

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
            return render(request,'superadmin/login.html',{'form':form,'msg':'Invalid Credientials'})
      else:
         return render(request,'superadmin/login.html',{'form':form})


class Index(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      return render(request,'superadmin/index.html')

   def post(self,request):
      pass