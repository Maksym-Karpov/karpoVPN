from django import template

register = template.Library()


@register.inclusion_tag('site_management/pagination_template.html')
def render_pagination(page_obj):
    return {'page_obj': page_obj}
