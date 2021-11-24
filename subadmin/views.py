from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from superadmin.forms import LoginForm
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from superadmin.views import language


class Login(View):
   
   def get(self,request):
      form = LoginForm
      return render(request,'login.html',{'form':form})

   def post(self,request):
      try:
         url = 'http://127.0.0.1:8000/adminapi/login'
         data = request.POST
         response = requests.post(url,data=data).json()
         request.session['token'] = response['key']
         return redirect(reverse('admin_index'))
      
      except Exception as e: 
         print(e)   
         pass
   
class Index(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      # request.session[settings.LANGUAGE_SESSION_KEY] = 'en'
      if request.GET.get('prefered_language'):
         language(request)
         
         return render(request,'index.html',{'lan':request.session['language']})
      request.session['language'] = 'en'
      return render(request,'index.html',{'is_admin':True})

class AllFarmer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      language(request)
      lan = request.session['language']
      token = 'Token'+ ' ' + str(request.session['token'])
      
      try:
         url = 'http://127.0.0.1:8000/adminapi/farmers'
         response = requests.get(url,headers={'Authorization': token }).json()
         print(response)
         return render(request,'show_farmer.html',{'is_admin':True,'results':response})
      
      except Exception as e: 
         print(e)   
         pass