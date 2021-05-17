from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    zoom = models.IntegerField(default=16)
    image = models.ImageField(upload_to='request_photos/%Y/%m/%d/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey('Response', on_delete=models.CASCADE)

    def __str__(self):
        return f'Request from {self.user.username} for "{self.latitude},{self.longitude},{self.zoom}"'


class Response(models.Model):
    image = models.ImageField(upload_to='response_photos/%Y/%m/%d/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response to "{Request.objects.get(response=self)}"'
