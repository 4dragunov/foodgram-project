from django.contrib import admin
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('email', 'first_name')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
