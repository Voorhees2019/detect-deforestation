from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Request(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    zoom = models.IntegerField(default=16)
    image = models.ImageField(upload_to='request_photos/%Y/%m/%d/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey('Response', on_delete=models.CASCADE)

    def __str__(self):
        return f'Request from {self.user.username} for "{self.latitude},{self.longitude},{self.zoom}"'

    def clean(self):
        if self.latitude < -90 or self.latitude > 90:
            raise ValidationError('Latitude must be in range [-90; 90]')
        if self.longitude < -180 or self.longitude > 180:
            raise ValidationError('Longitude must be in range [-180; 180]')
        if self.zoom < 1 or self.zoom > 21:
            raise ValidationError('Zoom must be in range [1; 21]')


class Response(models.Model):
    image = models.ImageField(upload_to='response_photos/%Y/%m/%d/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response to "{Request.objects.filter(response=self).first()}"'
