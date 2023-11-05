from django import forms

from site_management.models import Site


class SiteForm(forms.ModelForm):
    url = forms.URLField()

    class Meta:
        model = Site
        fields = (
            'name',
            'url'
        )
