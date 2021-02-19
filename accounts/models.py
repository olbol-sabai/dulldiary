from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from entries.models import Entry
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from PIL import Image


def upload_image_location(instance, filename):
    return f'img/profile_pics/{instance.username}/{filename}/'


class User(AbstractUser):
    country = CountryField()
    appreciated_entries = models.ManyToManyField(Entry, related_name='appreciated', blank=True)
    changed_perception_entries = models.ManyToManyField(Entry, related_name='changed_perc', blank=True)
    is_validated = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_location, max_length=300)

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    

