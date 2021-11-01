from django.contrib import admin
from .models import Farmer,Categories,Products


class SiteAdmin(admin.ModelAdmin):
   model = Farmer
   admin.site.site_header = 'Super Admin'
   exclude = ['deleted_at']


class CategoriesAdmin(admin.ModelAdmin):
   model = Categories
   exclude = ['deleted_at']

class ProductsAdmin(admin.ModelAdmin):
   model = Products
   exclude = ['deleted_at']

admin.site.register(Farmer,SiteAdmin)
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Products,ProductsAdmin)