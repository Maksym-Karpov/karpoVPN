from django.urls import path

from site_management import views

urlpatterns = [
    path(
        'create/',
        views.SiteCreateView.as_view(),
        name='site_create'
    ),
    path(
        'delete/<int:pk>/',
        views.SiteDeleteView.as_view(),
        name='site_delete'
    ),
    path(
        '',
        views.SiteListView.as_view(),
        name='site_list'
    ),
    path(
        'create/',
        views.SiteCreateView.as_view(),
        name='site_create'
    ),
    path(
        'statistic/',
        views.SiteStatisticListView.as_view(),
        name='site_statistic'
    )
]
