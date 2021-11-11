from django.contrib import admin
from .models import Address,Customer

# class AddressAdmin(admin.ModelAdmin):
#     model = Address
#     exclude= ['deleted_at']

#     # def get_extra(self, request, obj=None, **kwargs):
#     #     extra = 1
#     #     return extra


class UserAdmin(admin.ModelAdmin):
   model = Customer
   exclude= ['deleted_at']
#    inlines = [AddressAdmin,]

admin.site.register(Customer,UserAdmin)