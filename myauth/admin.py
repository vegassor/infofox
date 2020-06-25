from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'id', 'is_active', 'is_staff']

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: Set[str]
        hidden_fields = {'first_name', 'last_name'}
        # Prevent non-superusers from editing their own permissions
        if not is_superuser:
            disabled_fields |= {
                'login',
                'email',
                'password'
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'date_joined',
                'last_login',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(User, CustomUserAdmin)
