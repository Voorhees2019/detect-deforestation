from django.shortcuts import render
from .models import Request, Response
import urllib.request
from shutil import copyfileobj
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
import os


@login_required
def detect(request):
    return render(request, 'detection/detect.html', {})


@login_required
def detect_uploaded_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('uploaded_file')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        zoom = request.POST.get('zoom')

        url = f'https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size=600x600&maptype=satellite&key=AIzaSyDGHMwuICv6YA1GJvYS2tiodBVIgKPGzIU'
        with urllib.request.urlopen(url) as in_stream, open(f'sample1.jpg', 'wb') as out_file:
            copyfileobj(in_stream, out_file)

        # Processing
        # give image to neural network
        # get image back from neural network

        # save to database
        user_response = Response.objects.create(image=ImageFile(open('sample1.jpg', 'rb')))
        user_response.save()
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, zoom=zoom, image=uploaded_file,
                                              user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        if os.path.exists('sample1.jpg'):
            os.remove('sample1.jpg')

        return render(request, 'detection/result.html', {'user_request': user_request})
    else:
        return render(request, 'detection/detect.html', {})
