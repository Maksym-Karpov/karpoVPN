from django.contrib.auth import get_user_model
from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    default_path = models.CharField(max_length=255, default='/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        related_name='sites',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-created_at']
