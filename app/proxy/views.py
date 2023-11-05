import math
import sys
import urllib
from urllib.parse import urlparse

import redis
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from site_management.models import Site

SITE_VIEWS_COUNTER_VAR = 'site:{site_id}:views'
SITE_DATA_COUNTER_RECEIVED_VAR = 'site:{site_id}:rcvd_data'
SITE_DATA_COUNTER_UPLOADED_VAR = 'site:{site_id}:ul_data'

redis_conn = redis.StrictRedis(**settings.REDIS_CONNECTION)


class ProxySiteView(LoginRequiredMixin, View):
    def _build_url(self, domain: str, path: str) -> str:
        path = path if path.startswith('/') else '/' + path

        params = urllib.parse.urlencode(self.request.GET)
        pretty_params = '?' + params if params else ''

        url = 'https://' + domain + path + pretty_params
        return url

    @staticmethod
    def replace_tag_links_with_proxy(
            soup,
            domain,
            user_site_name,
            tag_name,
            tag_link_attr
    ):
        for anchor_tag in soup.find_all(tag_name):
            original_href: str = anchor_tag.get(tag_link_attr)
            if not original_href:
                continue
            path = urlparse(original_href).path
            query = urlparse(original_href).query
            original_href_domain = urlparse(original_href).netloc
            if domain == original_href_domain or original_href.startswith('/'):
                path = path + '?' + query if query else path
                internal_href = reverse('proxy_site',
                                        args=(user_site_name, path))

                anchor_tag[tag_link_attr] = internal_href
        return soup

    @staticmethod
    def _convert_bytes_to_kb(bytes):
        kilobyte = math.ceil(bytes / 1024)
        return kilobyte

    @staticmethod
    def site_views_increase(site_item):
        redis_conn.incr(SITE_VIEWS_COUNTER_VAR.format(site_id=site_item.id))

    def count_size_of_received_data(self, site_item, data_size_bytes):
        data_size_kb = self._convert_bytes_to_kb(bytes=data_size_bytes)
        redis_conn.incr(
            SITE_DATA_COUNTER_RECEIVED_VAR.format(site_id=site_item.id),
            data_size_kb
        )

    def count_size_of_uploaded_data(self, site_item, data_size_bytes):
        data_size_kb = self._convert_bytes_to_kb(bytes=data_size_bytes)
        redis_conn.incr(
            SITE_DATA_COUNTER_UPLOADED_VAR.format(site_id=site_item.id),
            data_size_kb
        )

    def get(self, request, *args, **kwargs):
        user_site_name = kwargs['user_site_name']
        path = kwargs.get('path', '/')

        site = get_object_or_404(Site, name=user_site_name, user=request.user)
        domain = site.domain

        content = requests.get(
            self._build_url(domain=domain, path=path)
        ).content

        if 'css' in path:
            return HttpResponse(content, content_type='text/css')
        if 'js' in path:
            return HttpResponse(content, content_type='application/javascript')
        if 'png' in path:
            return HttpResponse(content, content_type='image/png')
        if 'svg' in path:
            return HttpResponse(content, content_type='image/svg')
        if 'jpg' in path:
            return HttpResponse(content, content_type='image/jpeg')

        soup = BeautifulSoup(content, 'html.parser')
        self.replace_tag_links_with_proxy(
            soup=soup,
            domain=domain,
            user_site_name=user_site_name,
            tag_name='a',
            tag_link_attr='href'
        )
        self.replace_tag_links_with_proxy(
            soup=soup,
            domain=domain,
            user_site_name=user_site_name,
            tag_name='script',
            tag_link_attr='src'
        )
        self.replace_tag_links_with_proxy(
            soup=soup,
            domain=domain,
            user_site_name=user_site_name,
            tag_name='link',
            tag_link_attr='href'
        )
        self.replace_tag_links_with_proxy(
            soup=soup,
            domain=domain,
            user_site_name=user_site_name,
            tag_name='img',
            tag_link_attr='src'
        )

        modified_content = str(soup)
        self.site_views_increase(site_item=site)
        self.count_size_of_received_data(
            site_item=site,
            data_size_bytes=sys.getsizeof(modified_content)
        )
        return HttpResponse(modified_content)

    def post(self, request, *args, **kwargs):
        user_site_name = kwargs['user_site_name']
        site = get_object_or_404(Site, name=user_site_name, user=request.user)
        received_file = self.request.FILES.get('file')
        received_file_size = received_file.size if received_file else 0
        self.count_size_of_uploaded_data(
            site_item=site,
            data_size_bytes=received_file_size
        )
