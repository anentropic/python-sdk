from django.db import models


class FacebookUser(models.Model):
    uid = models.CharField(max_length=64, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=255)
    access_token = models.CharField(max_length=128)
