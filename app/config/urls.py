from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proxy/', include('proxy.urls')),
    path('accounts/', include('accounts.urls')),
    path('site_management/', include('site_management.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
