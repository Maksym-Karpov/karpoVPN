from django.urls import re_path

from proxy import views


urlpatterns = [
    re_path(
        r'^(?P<user_site_name>[\w-]+)(?P<path>/.*)?$',
        views.ProxySiteView.as_view(),
        name='proxy_site'
    ),
]
