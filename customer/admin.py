from django.contrib import admin
from .models import Address,Customer,Cart, Order

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

class OrderAdmin(admin.ModelAdmin):
   model = Order
   exclude= ['deleted_at']


admin.site.register(Customer,UserAdmin)
admin.site.register(Cart)
admin.site.register(Order,OrderAdmin)