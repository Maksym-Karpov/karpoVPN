from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserCountries(models.TextChoices):
    GERMANY = 'DEU', 'Germany (DEU)'
    FRANCE = 'FRA', 'France (FRA)'
    ITALY = 'ITA', 'Italy (ITA)'
    SPAIN = 'ESP', 'Spain (ESP)'
    GREECE = 'GRC', 'Greece (GRC)'
    UKRAINE = 'UKR', 'Ukraine (UKR)'


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"))
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    country = models.CharField(max_length=3, choices=UserCountries.choices)
    about = models.TextField()
