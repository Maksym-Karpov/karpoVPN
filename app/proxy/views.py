from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from services.proxy_service import ProxyService


class ProxySiteView(LoginRequiredMixin, View):
    def __init__(self):
        super().__init__()
        self.proxy_service = ProxyService()

    def get(self, request, *args, **kwargs):
        user_site_name = kwargs['user_site_name']
        path = kwargs.get('path', '/')

        return self.proxy_service.process_site_content(
            user_site_name=user_site_name,
            path=path,
            request_item=request
        )

    def post(self, request, *args, **kwargs):
        user_site_name = kwargs['user_site_name']
        return self.proxy_service.process_user_input_content(
            user_site_name=user_site_name,
            request_item=request
        )
