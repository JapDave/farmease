from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login,logout

from adminapi.views import CustomerRegister
from .forms import CategoryForm,CustomerUpdateForm, DistrictForm, LoginForm, OrderFieldForm, OrderForm, StateForm
from adminapi.models import SubAdmin
from customer.models import  Customer, Order,AddressForm
from farmer.models import Categories, Farmer, Products,State,District
from django.core.paginator import Paginator
from .forms import AdminForm,FarmerForm,CustomerForm,ProductForm
from django.utils import translation
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
      def authenticate(self, request, username=None, password=None, **kwargs):
         UserModel = get_user_model()
         
         try:
               user = UserModel.objects.get(email=username)
         except UserModel.DoesNotExist:
               return None
         else:
               if user.check_password(password):
                  return user
         return None


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
         email = form.cleaned_data.get("email")
         password = form.cleaned_data.get("password")
         user = EmailBackend.authenticate(self,request,username=email, password=password)
         if user is not None:
               login(request, user)
               return redirect(reverse('index'))
         else:            
            return render(request,'login.html',{'form':form,'msg':'Invalid Credientials'})
      else:
         return render(request,'login.html',{'form':form})

class Logout(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      logout(request)
      return redirect(reverse('login'))
      

class Index(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      # request.session[settings.LANGUAGE_SESSION_KEY] = 'en'
      if request.GET.get('prefered_language'):
         language(request)
         
         return render(request,'index.html',{'lan':request.session['language'],'is_admin':False})
      request.session['language'] = 'en'
      return render(request,'index.html',{'is_admin':False})

# State Section 
class AddState(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = StateForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_state.html',{'form':form,'lan':lan,'segment':'addstate'})

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
         return render(request,'add_state.html',{'form':form,'msg':msg,'lan':lan,'segment':'addstate'})
      except:
            if lan == 'gu':
               msg = 'રાજ્ય નથી ઉમેર્યું'
            else:
               msg = 'State Not Added'  
            return render(request,'add_state.html',{'form':form,'msg':msg,'lan':lan,'segment':'addstate'})

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
            return render(request,'show_state.html',{'results':state_data,'lan':lan,'segment':'allstate'})
         else:
            if lan == 'gu':
               msg = 'હજુ સુધી કોઈ રાજ્ય ઉમેર્યું નથી'
            else:
               msg = 'No State Added Yet'
            return render(request,'show_state.html',{'msg': msg,'lan':lan,'segment':'allstate' })
      except Exception as e :
         print(e)
         pass
         #404

class DeleteState(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      state = State.objects.get(_id=id)
      state.delete()
      return redirect(reverse('allstate'))

class UpdateState(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      state_obj = State.objects.get(_id=id)
      form = StateForm(instance = state_obj)
      language(request)
      lan = request.session['language']
      return render(request,'update_state.html',{'form':form,'lan':lan})
   
   def post(self,request,id):
      try:
         state_obj = State.objects.get(_id=id)
         form = StateForm(request.POST,instance=state_obj)
         language(request)
         lan = request.session['language']

         if lan == 'gu':
            msg = 'રાજ્ય અપડેટ'
         else:
            msg = 'State Updated'   
         form.is_valid()
         form.save()
         return render(request,'update_state.html',{'form':form,'msg':msg,'lan':lan})
      except:
            if lan == 'gu':
               msg = 'રાજ્ય નથી અપડેટ'
            else:
               msg = 'State Not Updated'  
            return render(request,'update_state.html',{'form':form,'msg':msg,'lan':lan})

# District Section

class AddDistrict(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = DistrictForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_district.html',{'form':form,'lan':lan,'segment':'adddistrict'})

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
        
         return render(request,'add_state.html',{'form':form,'msg':msg,'lan':lan,'segment':'adddistrict'})
      except:
         if lan == 'gu':
               msg = 'જિલ્લો નથી ઉમેર્યું'
         else:
            msg = 'District Not Added'   

         return render(request,'add_state.html',{'form':form,'msg': msg,'lan':lan,'segment':'adddistrict'})

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
           
            return render(request,'show_district.html',{'results':district_data,'lan':lan,'segment':'alldistrict'})
         else:
            if lan == 'gu':
               msg = 'હજુ સુધી કોઈ જિલ્લો ઉમેર્યું નથી'
            else: 
               msg = 'District Not Added yet'   
            return render(request,'show_district.html',{'msg': msg,'lan':lan,'segment':'alldistrict'})
      except:
         pass
         #404

class DeleteDistrict(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      district = District.objects.get(_id=id)
      district.delete()
      return redirect(reverse('alldistrict'))

class UpdateDistrict(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      district_obj = District.objects.get(_id=id)
      form = DistrictForm(instance = district_obj)
      language(request)
      lan = request.session['language']
      return render(request,'update_district.html',{'form':form,'lan':lan})

   
   def post(self,request,id):
      try:
         district_obj = District.objects.get(_id = id)
         form = DistrictForm(request.POST,instance = district_obj)
         language(request)
         lan = request.session['language']
         if lan == 'gu':
            msg = 'જિલ્લો અપડેટ'
         else:
            msg = 'District Updated'   

         form.is_valid()
         form.save()
        
         return render(request,'update_district.html',{'form':form,'msg':msg,'lan':lan})
      except:
         if lan == 'gu':
               msg = 'જિલ્લો નથી અપડેટ'
         else:
            msg = 'District Not Updated'   

         return render(request,'update_district.html',{'form':form,'msg': msg,'lan':lan})

# Category Section 

class AddCategory(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):
      form = CategoryForm()     
      language(request)
      lan = request.session['language']

      return render(request,'add_category.html',{'form':form,'lan':lan,'segment':'addcategory'})

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
         return redirect(reverse('allcategory'))
      except:
         if lan == 'gu':
            msg = 'શ્રેણીઓ નથી ઉમેર્યું'
         else:
            msg = 'Category Not Added'   
         return render(request,'add_category.html',{'form':form,'msg':msg,'lan':lan,'segment':'addcategory'})

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
            return render(request,'show_category.html',{'results':category_data,'lan':lan,'segment':'allcategory'})
         else:
            if lan == 'gu':
               msg = 'હજુ સુધી કોઈ શ્રેણી ઉમેરાઈ નથી'
            else:
               msg = 'No Category Added Yet'
            return render(request,'show_category.html',{'lan':lan,'msg':msg,'segment':'allcategory'})
      except Exception as e:
         
         pass
         #404

class DeleteCategory(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      category = Categories.objects.get(_id=id)
      category.delete()
      return redirect(reverse('allcategory'))

class UpdateCategory(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         category_obj = Categories.objects.get(_id = id)
         form = CategoryForm(instance = category_obj)
         language(request)
         lan = request.session['language']
         return render(request,'update_category.html',{'form':form,'lan':lan})
      except Exception as e:
         pass
         #404

   def post(self,request,id):
      try:
         category_obj = Categories.objects.get(_id = id)
         form = CategoryForm(request.POST,request.FILES,instance = category_obj)
         form.is_valid()
         form.save()
         language(request)
         lan = request.session['language']

         if lan == 'gu':
            msg = 'શ્રેણીઓ અપડેટ કર્યું'
         else:
            msg = 'Category Updated'   
         return redirect(reverse('allcategory'))
      except:
         if lan == 'gu':
               msg = 'શ્રેણીઓ નથી અપડેટ કર્યું'
         else:
            msg = 'Category Not Updated'   
         return render(request,'update_category.html',{'form':form,'msg':msg,'lan':lan})


# Admin Section 

class AddAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = AdminForm()
      language(request)
      lan = request.session['language']


      return render(request,'add_admin.html',{'form':form,'lan':lan,'segment':'addadmin'})

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
         return redirect(reverse('alladmin'))
      except:
         if lan == 'gu':
               msg = 'એડમિન નથી ઉમેરાયો'
         else:
            msg = 'Admin Not Added'   
         return render(request,'add_admin.html',{'form':form,'msg': msg,'lan':lan,'segment':'addadmin'})
 
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
            return render(request,'show_admin.html',{'results':admin_data,'lan':lan,'segment':'alladmin'})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ એડમિન ઉમેરાઈ નથી'
            else:
               msg = 'No Admin Added Yet'
            return render(request,'show_admin.html',{'msg': msg,'lan':lan,'segment':'alladmin'})
      except Exception as e:
         print(e)
         pass

class DeleteAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      admin= SubAdmin.objects.get(_id=id)
      admin.delete()
      return redirect(reverse('alladmin'))

class UpdateAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         admin_obj = SubAdmin.objects.get(_id = id)
         form = AdminForm(instance = admin_obj)
         language(request)
         lan = request.session['language']
         return render(request,'update_admin.html',{'form':form,'lan':lan})
      except Exception as e:
         pass
         #404

   def post(self,request,id):
      try:
         admin_obj = SubAdmin.objects.get(_id = id)
         form = AdminForm(request.POST,request.FILES,instance = admin_obj)
         form.is_valid()
         form.save()
         language(request)
         lan = request.session['language']

         if lan == 'gu':
            msg = 'એડમિન અપડેટ કર્યું'
         else:
            msg = 'Admin Updated'   
         return redirect(reverse('alladmin'))
      except:
         if lan == 'gu':
               msg = 'એડમિન નથી અપડેટ કર્યું'
         else:
            msg = 'Admin Not Updated'   
         return render(request,'update_admin.html',{'form':form,'msg':msg,'lan':lan})

class DetailAdmin(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         admin_obj = SubAdmin.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         return render(request,'detail_admin.html',{'admin':admin_obj,'lan':lan})
      except Exception as e:
         print(e)
         pass


# Farmer Section

class AddFarmer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = FarmerForm()
      language(request)
      lan = request.session['language']      

      return render(request,'add_farmer.html',{'form':form,'lan':lan,'segment':'addfarmer'})

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
         
         return redirect(reverse('allfarmer'))
      except Exception as e:
       
         if lan == 'gu':
               msg = 'ખેડૂત નથી ઉમેરાયો'
         else:
            msg = 'Farmer Not Added'   
         return render(request,'add_farmer.html',{'form':form,'msg': msg,'lan':lan,'segment':'addfarmer'})
 
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
            return render(request,'show_farmer.html',{'results':farmer_data,'lan':lan,'segment':'allfarmer'})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ખેડૂત ઉમેરાઈ નથી'
            else:
               msg = 'No Farmer Added Yet'
            return render(request,'show_farmer.html',{'msg': msg,'lan':lan,'segment':'allfarmer'})
      except:
         pass

class DeleteFarmer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      farmer = Farmer.objects.get(_id=id)
      farmer.delete()
      return redirect(reverse('allfarmer'))

class UpdateFarmer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      farmer_obj = Farmer.objects.get(_id=id)
      form = FarmerForm(instance = farmer_obj)
      language(request)
      lan = request.session['language']
      return render(request,'update_farmer.html',{'form':form,'lan':lan})

   def post(self,request,id):
      try:
         farmer_obj = Farmer.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         
         if lan == 'gu':
            msg = 'ખેડૂત અપડેટ કર્યું'
         else:
            msg = 'Farmer Updated' 
         form  = FarmerForm(request.POST,request.FILES,instance = farmer_obj)
         form.is_valid()
         form.save()
         return redirect(reverse('allfarmer'))
      except:
         if lan == 'gu':
               msg = 'ખેડૂત નથી અપડેટ'
         else:
            msg = 'Farmer Not Updated'   
         return render(request,'update_farmer.html',{'form':form,'msg': msg,'lan':lan})

class DetailFarmer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         farmer_obj = Farmer.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         return render(request,'detail_farmer.html',{'farmer':farmer_obj,'lan':lan})
      except Exception as e:
         print(e)
         pass


# Customer Section 

class AddCustomer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = CustomerForm()
      addressform = AddressForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_customer.html',{'form':form,'addressform':addressform,'lan':lan,'segment':'addcustomer'})

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

         return redirect(reverse('allcustomer'))
      except Exception as e:
         if lan == 'gu':
               msg = 'ગ્રાહક નથી ઉમેરાયો'
         else:
            msg = 'Customer Not Added'   
         return render(request,'add_customer.html',{'form':form,'addressform':addressform,'msg': msg,'lan':lan,'segment':'addcustomer'})
 
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
            return render(request,'show_customer.html',{'results':customer_data,'lan':lan,'segment':'allcustomer'})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ગ્રાહક ઉમેરાઈ નથી'
            else:
               msg = 'No Customer Added Yet'
            return render(request,'show_customer.html',{'msg': msg,'lan':lan,'segment':'allcustomer'})
      except Exception as e:
         print(e)
         pass

class DeleteCustomer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      customer = Customer.objects.get(_id=id)
      customer.delete()
      return redirect(reverse('allcustomer'))

class UpdateCustomer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):  
      customer_obj = Customer.objects.get(_id = id)
      form = CustomerUpdateForm(instance=customer_obj)  
      language(request)
      lan = request.session['language']
      return render(request,'update_customer.html',{'form':form,'lan':lan})

   def post(self,request,id):
      try:
         customer_obj = Customer.objects.get(_id = id) 
         language(request)
         lan = request.session['language']
         if lan == 'gu':
            msg = 'ગ્રાહક અપડેટ'
         else:
            msg = 'Customer Updated' 
         form  = CustomerUpdateForm(request.POST,request.FILES,instance=customer_obj)
         form.is_valid()
         form.save() 
         return redirect(reverse('allcustomer'))
      except Exception as e:
         print(e)
         if lan == 'gu':
               msg = 'ગ્રાહક નથી અપડેટ'
         else:
            msg = 'Customer Not Updated'   
         return render(request,'update_customer.html',{'form':form,'msg': msg,'lan':lan})

class DetailCustomer(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         customer_obj = Customer.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         return render(request,'detail_customer.html',{'customer':customer_obj,'lan':lan})
      except:
         pass

class AddAddress(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,customer_id):
      try:        
        
         form = AddressForm()
         language(request)
         lan = request.session['language']
         return render(request,'add_address.html',{'form':form,'lan':lan})
      except Exception as e:
         pass 
   
   def post(self,request,customer_id):
      try:        
         customer_obj = Customer.objects.get(_id=customer_id)       
         form = AddressForm(request.POST)
         form.is_valid()
         address_obj = form.save(commit=False)
         customer_obj.addresses.append(address_obj)
         customer_obj.save()
         language(request)
         lan = request.session['language']
         if lan == 'gu':
            msg = 'સરનામું ઉમેરાયો'
         else:
            msg = 'Address Added' 
         return render(request,'add_address.html',{'form':form,'lan':lan,'msg':msg})
      except Exception as e:
         print(e)
         pass 

class AddressView(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         customer_obj = Customer.objects.get(_id = id )
         address_list = []
         language(request)
         lan = request.session['language']

         for item in customer_obj.addresses:
            address_list.append(item)   
               
         page = request.GET.get('page',1)
         paginator = Paginator(address_list,10)
         customer_data = paginator.page(page)
         return render(request,'show_address.html',{'customer_id':id,'addresses':customer_data,'lan':lan})
        
      except Exception as e:
         print(e)
         pass

class UpdateAddress(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,customer_id,id):
      try:        
         customer_obj = Customer.objects.get(_id=customer_id)
         for add in customer_obj.addresses:
            if str(add._id) == id:
                  data = add
                  break
         form = AddressForm(instance=data)
         language(request)
         lan = request.session['language']
         return render(request,'update_address.html',{'form':form,'lan':lan})
      except Exception as e:
         pass 
   
   def post(self,request,customer_id,id):
      try:        
         customer_obj = Customer.objects.get(_id=customer_id)
         counter = 0
         for add in customer_obj.addresses:           
            if str(add._id) == id:
                  data = add
                  break
            counter += 1
         form = AddressForm(request.POST,instance=data)
         form.is_valid()
         address_obj = form.save(commit=False)
         customer_obj.addresses[counter] = address_obj
         customer_obj.save()
         language(request)
         lan = request.session['language']
         if lan == 'gu':
            msg = 'સરનામું અપડેટ'
         else:
            msg = 'Address Updated' 
         return render(request,'update_address.html',{'form':form,'lan':lan,'msg':msg})
      except Exception as e:
         print(e)
         pass 

class DeleteAddress(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,customer_id,id):
      customer_obj = Customer.objects.get(_id=customer_id)
      for add in customer_obj.addresses:
         if str(add._id) == id:
               data = add
               break
      try:
         customer_obj.addresses.remove(data)
         customer_obj.save()
         return redirect(reverse('alladdress',kwargs={'id':customer_id}))
      except Exception as e:
         pass 


# Product Section 

class AddProduct(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = ProductForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_product.html',{'form':form,'lan':lan,'segment':'addproduct'})

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
         return redirect(reverse('allproduct'))
      except:
         if lan == 'gu':
               msg = 'ઉત્પાદનો નથી ઉમેરાયો'
         else:
            msg = 'Product Not Added'   
         return render(request,'add_product.html',{'form':form,'msg': msg,'lan':lan,'segment':'addproduct'})
 
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
            return render(request,'show_product.html',{'results':product_data,'lan':lan,'segment':'allproduct'})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ઉત્પાદનો ઉમેરાઈ નથી'
            else:
               msg = 'No Product Added Yet'
            return render(request,'show_product.html',{'msg': msg,'lan':lan,'segment':'allproduct'})
      except Exception as e:
         print(e)
         pass  

class DeleteProduct(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      product = Products.objects.get(_id=id)
      product.delete()
      return redirect(reverse('allproduct'))

class UpdateProduct(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      product_obj = Products.objects.get(_id=id)
      form = ProductForm(instance = product_obj)
      language(request)
      lan = request.session['language']
      return render(request,'update_product.html',{'form':form,'lan':lan})

   def post(self,request,id):
      try:
         product_obj = Products.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         
         if lan == 'gu':
            msg = 'ઉત્પાદનો અપડેટ કર્યું'
         else:
            msg = 'Product Updated' 
         form  = ProductForm(request.POST,request.FILES,instance = product_obj)
         form.is_valid()
         form.save()
         return redirect(reverse('allproduct'))
      except:
         if lan == 'gu':
               msg = 'ઉત્પાદનો નથી અપડેટ'
         else:
            msg = 'Product Not Updated'   
         return render(request,'update_product.html',{'form':form,'msg': msg,'lan':lan})

class DetailProduct(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         product_obj = Products.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         return render(request,'detail_product.html',{'product':product_obj,'lan':lan})
      except Exception as e:
         print(e)
         pass

# Order Section 

class AddOrder(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request):  
      form = OrderForm()
      orderfieldform = OrderFieldForm()
      language(request)
      lan = request.session['language']
      return render(request,'add_order.html',{'form':form,'itemform':orderfieldform,'lan':lan,'segment':'addorder'})

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
           
         
         return render(request,'add_order.html',{'form':form,'itemform':orderfieldform,'msg': msg,'lan':lan,'segment':'addorder'})
      except Exception as e:
     
         if lan == 'gu':
               msg = 'ઓર્ડર નથી ઉમેરાયો'
         else:
            msg = 'Order Not Added'   
         return render(request,'add_order.html',{'form':form,'itemform':orderfieldform,'msg': msg,'lan':lan,'segment':'addorder'})
 
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
            return render(request,'show_order.html',{'results':order_data,'lan':lan,'segment':'allorder'})
         else:
            if lan == 'gu':
                  msg = 'હજુ સુધી કોઈ ઓર્ડર ઉમેરાઈ નથી'
            else:
               msg = 'No Orders Added Yet'
            return render(request,'show_order.html',{'msg': msg,'lan':lan,'segment':'allorder'})
      except:
         pass  

class DeleteOrder(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      order = Order.objects.get(_id=id)
      order.delete()
      return redirect(reverse('allorder'))

class UpdateOrder(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      order_obj = Order.objects.get(_id=id)
      form = OrderForm(instance = order_obj)
      language(request)
      lan = request.session['language']
      return render(request,'update_order.html',{'form':form,'lan':lan})

   def post(self,request,id):
      try:
         order_obj = Order.objects.get(_id=id)    
         language(request)
         lan = request.session['language']
         
         if lan == 'gu':
            msg = 'ઓર્ડર અપડેટ કર્યું'
         else:
            msg = 'order Updated' 
         form  = OrderForm(request.POST,request.FILES,instance = order_obj)
         form.is_valid()
         form.save()
         return render(request,'update_order.html',{'form':form,'msg': msg,'lan':lan})
      except:
         if lan == 'gu':
               msg = 'ઓર્ડર નથી અપડેટ'
         else:
            msg = 'Order Not Updated'   
         return render(request,'update_order.html',{'form':form,'msg': msg,'lan':lan})

class DetailOrder(LoginRequiredMixin,View):
   login_url = 'login'

   def get(self,request,id):
      try:
         order_obj = Order.objects.get(_id=id)
         language(request)
         lan = request.session['language']
         return render(request,'detail_order.html',{'order':order_obj,'lan':lan})
      except Exception as e:
         print(e)
         pass