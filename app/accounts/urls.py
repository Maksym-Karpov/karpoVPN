from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views


urlpatterns = [
    path(
        'registration/',
        views.UserSignUpView.as_view(),
        name='registration'
    ),
    path(
        'login/',
        LoginView.as_view(template_name="accounts/login.html"),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
    path(
        'profile/<int:pk>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
    path(
        'profile/<int:pk>/edit',
        views.ProfileEditView.as_view(),
        name='profile_edit'
    ),

    path(
        'custom_login_redirect/',
        views.LoginRedirectView.as_view(),
        name='custom_login_redirect'
    ),
]
