from django.contrib import admin

from users.models import UsersProfile


@admin.register(UsersProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code', 'auth_code')
