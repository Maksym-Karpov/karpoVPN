from django.contrib.auth import get_user_model, forms
from django import forms as form

User = get_user_model()


class CustomUserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'country',
            'about'
        )


class UserChangeForm(form.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'about',
            'country',
        )
