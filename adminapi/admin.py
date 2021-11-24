from django.contrib import admin
from .models import SubAdmin

class UserAdmin(admin.ModelAdmin):
   model = SubAdmin
   exclude= ['deleted_at']



admin.site.register(SubAdmin,UserAdmin)
