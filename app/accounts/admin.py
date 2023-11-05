from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', )
        }),
        ('About', {
            'fields': ('about',)
        }),
        ('Country', {
            'fields': ('country',)
        }),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('About', {
            'fields': ('about',)
        }),
        ('Country', {
            'fields': ('country',)
        }),
    )
    list_display = ('username', 'first_name', 'last_name')
