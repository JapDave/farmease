from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from requests.api import request
from superadmin.forms import AddressForm, CustomerForm, LoginForm,FarmerForm
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from superadmin.views import language
from django.core.paginator import Paginator
from farmer.models import Farmer,State,District
from customer.models import Customer,Categories

class Login(View): 
   def get(self,request):
      form = LoginForm
      return render(request,'login.html',{'form':form})

   def post(self,request):
      try:
         url = 'http://127.0.0.1:8000/adminapi/login'
         data = request.POST
         response = requests.post(url,data=data).json()
         request.session['token'] = 'Token'+ ' ' + response['key']
         return redirect(reverse('admin_index'))
      
      except Exception as e:  
         form = LoginForm
         msg = 'Wrong Credentials'
         return render(request,'login.html',{'form':form,'msg':msg})
   
class Logout(View):
   def get(self,request):
      try:
         url = 'http://127.0.0.1:8000/adminapi/logout'
         token = request.session['token']
         response = requests.post(url,data={'token':token.split()},headers={'Authorization': token }).json() 
         if 'success' in response:
            del request.session['token']
            return redirect(reverse('admin_login'))  
         else:
            pass 
            #404 
      except:
         return redirect(reverse('admin_index'))

class Index(View):
   def get(self,request):
      if request.session['token']:
      # request.session[settings.LANGUAGE_SESSION_KEY] = 'en'
         if request.GET.get('prefered_language'):
            language(request)
            context = {
                     'is_admin':True,
                     'lan':request.session['language'],
                     'segment':'index'
                  }
            return render(request,'index.html',context)
         request.session['language'] = 'en'
         return render(request,'index.html',{'is_admin':True})
      else:
         return redirect(reverse('admin_login'))

class CategoryView(View): 
   def get(self,request):
      if request.session['token']:
         try:
            category_obj = Categories.objects.all()
            language(request)
            lan = request.session['language']

            if category_obj:
               page = request.GET.get('page',1)
               paginator = Paginator(category_obj,10)
               category_data = paginator.page(page)
               context = {
                  'results':category_data,
                  'lan':lan,
                  'is_admin':True,
                  'segment':'category'
               }
               return render(request,'show_category.html',context)
            else:
               if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ શ્રેણી ઉમેરાઈ નથી'
               else:
                  msg = 'No Category Added Yet'
               context = {
                  'msg':msg,
                  'lan':lan,
                  'is_admin':True,
                  'segment':'category'
               }
               return render(request,'show_category.html',context)
         except Exception as e:
            pass
            #404
      else:
         return redirect(reverse('login'))

class StateView(View):
   login_url = 'login'

   def get(self,request):
      if request.session['token']:
         try:
            state_obj = State.objects.all()
            language(request)
            lan = request.session['language']
            
            if state_obj:
               page = request.GET.get('page',1)
               paginator = Paginator(state_obj,10)
               state_data = paginator.page(page)
               context = {
                  'results':state_data,
                  'lan':lan,
                  'is_admin':True,
                  'segment':'state'
               }
               return render(request,'show_state.html',context)
            else:
               if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ રાજ્ય ઉમેર્યું નથી'
               else:
                  msg = 'No State Added Yet'
                  context = {
                  'msg':msg,
                  'lan':lan,
                  'is_admin':True,
                  'segment':'state'
               }
               return render(request,'show_state.html',context)
         except Exception as e :
            print(e)
            pass
            #404
      else:
         return redirect(reverse('login'))

class DistrictView(View):
   def get(self,request):
      if request.session['token']:
         try:
            district_obj = District.objects.all()
            language(request)
            lan = request.session['language']
            
            if district_obj:
               page = request.GET.get('page',1)
               paginator = Paginator(district_obj,10)
               district_data = paginator.page(page)
               context = {
                  'results':district_data,
                  'lan':lan,
                  'is_admin':True,
                  'segment':'district'
               }
               return render(request,'show_district.html',context)
            else:
               if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ જિલ્લો ઉમેર્યું નથી'
               else: 
                  msg = 'District Not Added yet' 
                  context = {
                  'msg': msg,
                  'lan':lan,
                  'is_admin':True,
                  'segment':'district'
               }  
               return render(request,'show_district.html',context)
         except:
            pass
            #404
      else:
         return redirect('login')


# Farmer Section
class FarmerView(View):
  
   def get(self,request):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/farmers'
         try:
            response = requests.get(url,headers={'Authorization': token }).json()  
         except:
            return redirect(reverse('login'))     
         page = request.GET.get(response['current page'],1)
         paginator = Paginator(response['results'],10)
         farmer_data = paginator.page(page)
         context = {
                  'is_admin':True,
                  'lan':lan,
                  'segment':'showfarmer',
                  'results':farmer_data
               }
         return render(request,'show_farmer.html',context)
      except Exception as e: 
         pass

class AddFarmer(View):
   def get(self,request):  
      form = FarmerForm()
      language(request)
      lan = request.session['language']      
      context = {
                  'is_admin':True,
                  'lan':lan,
                  'segment':'addfarmer',
                  'form':form
               }
      return render(request,'add_farmer.html',context)

   def post(self,request):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/addfarmer'
         try:
            response = requests.post(url,data=request.POST,files=request.FILES,headers={'Authorization': token }).json()
         except:
            return redirect(reverse('login'))
         if 'detail' in response:
            form = FarmerForm(request.POST)     
            context = {
                  'is_admin':True,
                  'lan':lan,
                  'segment':'addfarmer',
                  'form':form
               }
            return render(request,'add_farmer.html',context)  
         elif response['user']:
            return redirect(reverse('admin_allfarmer'))
      except Exception as e:
         print(e)
         pass 

class DetailFarmer(View):
   def get(self,request,id):
      language(request)
      lan = request.session['language']
      token = request.session['token']

      try:
         url = 'http://127.0.0.1:8000/adminapi/farmerdetail/'+id
         try:
           response = requests.get(url,headers={'Authorization': token }).json()
         except:
            return redirect(reverse('login'))
         context = {
                  'is_admin':True,
                  'lan':lan,
                  'segment':'farmer',
                  'farmer':response['farmer']
               }
         if 'farmer' in response:
            return render(request,'detail_farmer.html',context)
         else:
            pass
      except Exception as e:
         pass

class UpdateFarmer(View):

   def get(self,request,id):
      farmer_obj = Farmer.objects.get(_id=id)
      form = FarmerForm(instance = farmer_obj)
      language(request)
      lan = request.session['language']
      context = {
               'is_admin':True,
               'lan':lan,
               'segment':'farmer',
               'form': form,
               
               }
      return render(request,'update_farmer.html',context)

   def post(self,request,id):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/farmerdetail/'+id
         try:
            response = requests.post(url,data=request.POST,files=request.FILES,headers={'Authorization': token }).json()   
         except:
            return redirect(reverse('login'))
         if 'detail' in response:
            form = FarmerForm(request.POST)     
            return render(request,'update_farmer.html',{'form':form,'lan':lan,'is_admin':True})      
         else:
            return redirect(reverse('admin_detailfarmer',kwargs={'id':id}))
      except Exception as e:
         pass 

class DeleteFarmer(View):
   def get(self,request,id):
      try:
         language(request)
         lan = request.session['language']
         token = request.session['token']
         url = 'http://127.0.0.1:8000/adminapi/farmerdetail/'+id
         try:
            response = requests.delete(url,headers={'Authorization': token }).json()   
         except:
            return redirect(reverse('login'))
         if 'success' in response:
            return redirect(reverse('admin_allfarmer'))
         else:
            pass
      except Exception as e:
         print(e)
         pass


# Customer Section
class CustomerView(View):
   def get(self,request):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/customers'
         try:
            response = requests.get(url,headers={'Authorization': token }).json()       
         except:
            return redirect(reverse('login'))
         page = request.GET.get(response['current page'],1)
         paginator = Paginator(response['customers'],10)
         customer_data = paginator.page(page)
         context = {
                  'is_admin':True,
                  'lan':lan,
                  'segment':'showcustomer',
                  'results':customer_data
               }
         return render(request,'show_customer.html',context)
      except Exception as e: 
         pass

class AddCustomer(View):
   def get(self,request):  
      form = CustomerForm()
      addressform = AddressForm()
      language(request)
      lan = request.session['language']      
      context = {
               'is_admin':True,
               'lan':lan,
               'segment':'addcustomer',
               'form': form,
               'addressform':addressform
               }
      return render(request,'add_customer.html',context)

   def post(self,request):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/addcustomer'
         try:
            response = requests.post(url,data=request.POST,files=request.FILES,headers={'Authorization': token }).json()
         except:
            return redirect(reverse('login'))

         if 'detail' in response:
            form = CustomerForm(request.POST)     
            addressform = AddressForm(request.POST)
            context = {
               'is_admin':True,
               'lan':lan,
               'segment':'addcustomer',
               'form': form,
               'addressform':addressform
               }
            return render(request,'add_customer.html',context)
            
         elif response['user']:
            return redirect(reverse('allcustomer'))
      except Exception as e:
         pass 

class DetailCustomer(View):
   def get(self,request,id):
      language(request)
      lan = request.session['language']
      token = request.session['token']

      try:
         url = 'http://127.0.0.1:8000/adminapi/customerdetail/'+id
         try:
            response = requests.get(url,headers={'Authorization': token }).json()
         except:
            return redirect(reverse('login'))
         if 'customer' in response:
            context = {
               'is_admin':True,
               'lan':lan,
               'segment':'addcustomer',
               'customer':response['customer']
               }
            return render(request,'detail_customer.html',context)
         else:
            pass
      except Exception as e:
         pass

class UpdateCustomer(View):

   def get(self,request,id):
      customer_obj = Customer.objects.get(_id=id)
      form = CustomerForm(instance = customer_obj)
      language(request)
      lan = request.session['language']
      context = {
               'is_admin':True,
               'lan':lan,
               'segment':'customer',
               'form': form,
               }
      return render(request,'update_customer.html',context)

   def post(self,request,id):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/customerdetail/'+id
         try:
            response = requests.post(url,data=request.POST,files=request.FILES,headers={'Authorization': token }).json()   
         except:
            return redirect(reverse('login'))
         if 'detail' in response:
            pass
         else:
            return redirect(reverse('admin_allcustomer'))
      except Exception as e:
         pass 

class DeleteCustomer(View):
   def get(self,request,id):
      try:
         language(request)
         lan = request.session['language']
         token = request.session['token']
         url = 'http://127.0.0.1:8000/adminapi/customerdetail/'+id
         try:
            response = requests.delete(url,headers={'Authorization': token }).json()   
         except:
            return redirect(reverse('login'))
         if 'success' in response:
            return redirect(reverse('admin_allfarmer'))
         else:
            pass
      except Exception as e:
         print(e)
         pass


# Product Section
class ProductView(View):
 
   def get(self,request):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/products'
         try:
            response = requests.get(url,headers={'Authorization': token }).json()       
         except:
            return redirect(reverse('login'))
         page = request.GET.get(response['current page'],1)
         paginator = Paginator(response['results'],10)
         product_data = paginator.page(page)
         context = {
               'is_admin':True,
               'lan':lan,
               'segment':'showproduct',
               'results':product_data
               }
         return render(request,'show_product.html',context)
      except Exception as e: 
         pass

class DetailProduct(View):
   
   def get(self,request,id):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/productdetail/'+id
         try:
            response = requests.get(url,headers={'Authorization': token }).json()      
         except:
            return redirect(reverse('login'))
         if 'product' in response:
            context = {
            'is_admin':True,
            'lan':lan,
            'segment':'product',
            'product':response['product']
            }
            return render(request,'detail_product.html',context)
      except Exception as e: 
         pass

class DeleteProduct(View):

   def get(self,request,id):
      pass


# Order Section
class OrderView(View):
   def get(self,request):
      language(request)
      lan = request.session['language']
      token = request.session['token']
      try:
         url = 'http://127.0.0.1:8000/adminapi/farmers'
         try:
            farmer_response = requests.get(url,headers={'Authorization': token}).json() 
         except:
            return redirect(reverse('login'))
         context = {
            'is_admin':True,
            'lan':lan,
            'segment':'order',
            'farmers':farmer_response['results'],
         } 
         if request.GET.get('selected_farmer'):
            id = request.GET.get('selected_farmer')
            url = 'http://127.0.0.1:8000/adminapi/orderhistory/'+id
            try:
               order_response = requests.get(url,headers={'Authorization': token }).json()
            except:
               return redirect(reverse('login'))
            page = request.GET.get(order_response['current page'],1)
            paginator = Paginator(order_response['orders'],10)
            order_data = paginator.page(page)
            context['orders'] = order_data
            context['selected_farmer'] = id   
         return render(request,'admin/orders.html',context)
      except Exception as e: 
         pass


class OrderDetail(View):
   def get(self,request,id):
      try:
         language(request)
         lan = request.session['language']
         token = request.session['token']
         url = 'http://127.0.0.1:8000/adminapi/orderdetail/'+id
         try:
            response = requests.get(url,headers={'Authorization': token }).json()
         except:
            return redirect(reverse('allorder'))
         if 'order' in response:
            context = {
               'is_admin':True,
               'segment':'order',
               'order':response['order'],
               'lan':lan
            }
            return render(request,'detail_order.html',context)
         else:
            return redirect(reverse('allorder'))
      except Exception as e:
         print(e)
         pass