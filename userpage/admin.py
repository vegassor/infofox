from django.contrib import admin
from .models import InfoBlock, Profile, Bracelet


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'id')


class InfoBlockAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'id')


class BraceletAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'unique_code')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Bracelet, BraceletAdmin)
admin.site.register(InfoBlock, InfoBlockAdmin)
