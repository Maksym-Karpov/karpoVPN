import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from proxy.mixin import FilterSitesByUserMixin
from proxy.views import SITE_VIEWS_COUNTER_VAR, SITE_DATA_COUNTER_RECEIVED_VAR, \
    SITE_DATA_COUNTER_UPLOADED_VAR
from site_management.forms import SiteForm
from site_management.models import Site

redis_conn = redis.StrictRedis(**settings.REDIS_CONNECTION)


class SiteCreateView(LoginRequiredMixin, CreateView):
    model = Site
    template_name = 'site_management/site_create.html'
    form_class = SiteForm
    success_url = reverse_lazy('site_list')

    def form_valid(self, form):
        from urllib.parse import urlparse
        url = form.cleaned_data['url']
        parsed_url = urlparse(url)
        path = parsed_url.path
        domain = parsed_url.netloc
        if Site.objects.filter(domain=domain).exists():
            messages.error(
                self.request,
                f'Site with {domain} already exists'
            )
            return super().form_invalid(form)

        form.instance.domain = domain
        form.instance.default_path = path
        form.instance.user = self.request.user
        return super().form_valid(form=form)


class SiteListView(LoginRequiredMixin, FilterSitesByUserMixin, ListView):
    model = Site
    template_name = 'site_management/site_list.html'
    context_object_name = 'sites'
    paginate_by = 5


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    success_url = reverse_lazy('site_list')
    template_name = 'site_management/site_confirm_delete.html'


class SiteStatisticListView(
    LoginRequiredMixin,
    FilterSitesByUserMixin,
    ListView
):
    model = Site
    context_object_name = 'sites'
    template_name = 'site_management/site_statistic_list.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()
        site_view_statistics = {}
        site_ul_data_statistics = {}
        site_rcvd_data_statistics = {}

        for site in self.object_list:
            total_views = redis_conn.get(
                SITE_VIEWS_COUNTER_VAR.format(site_id=site.id)
            )
            uploaded_total_data = redis_conn.get(
                SITE_DATA_COUNTER_UPLOADED_VAR.format(site_id=site.id)
            )
            received_total_data = redis_conn.get(
                SITE_DATA_COUNTER_RECEIVED_VAR.format(site_id=site.id)
            )

            site_view_statistics[site.id] = self._pretty_numeric_value(
                value=total_views
            )

            site_ul_data_statistics[site.id] = self._pretty_numeric_value(
                value=uploaded_total_data
            )
            site_rcvd_data_statistics[site.id] = self._pretty_numeric_value(
                value=received_total_data
            )

        context_data['site_view_statistics'] = site_view_statistics
        context_data['site_ul_data_statistics'] = site_ul_data_statistics
        context_data['site_rcvd_data_statistics'] = site_rcvd_data_statistics
        return context_data

    @staticmethod
    def _pretty_numeric_value(value):
        return int(value) if value else 0
