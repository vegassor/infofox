from django.contrib import admin
from .models import *


admin.site.register(User)

# from django.contrib.auth.admin import UserAdmin
# from django.contrib import admin
# from .models import User
#
#
# class MyUserAdmin(UserAdmin):
#     model = User
#
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('password',)}),
#     )
#
#
# admin.site.register(User, MyUserAdmin)
