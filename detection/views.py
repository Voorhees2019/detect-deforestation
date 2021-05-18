from django.shortcuts import render, get_object_or_404
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

        url = f'https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size=640x640&maptype=satellite&key=AIzaSyDGHMwuICv6YA1GJvYS2tiodBVIgKPGzIU'
        with urllib.request.urlopen(url) as in_stream, open(f'sample1.jpg', 'wb') as out_file:
            copyfileobj(in_stream, out_file)

        # Processing
        # give image to neural network
        # get image back from neural network

        # save response to database
        user_response = Response.objects.create(image=ImageFile(open('sample1.jpg', 'rb')))
        user_response.save()
        # save request to database
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, zoom=zoom, image=uploaded_file,
                                              user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        if os.path.exists('sample1.jpg'):
            os.remove('sample1.jpg')

        return render(request, 'detection/result.html', {'user_request': user_request})
    else:
        return render(request, 'detection/detect.html', {})


@login_required
def detect_on_map(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        zoom = request.POST.get('zoom')

        url = f'https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size=640x640&maptype=satellite&key=AIzaSyDGHMwuICv6YA1GJvYS2tiodBVIgKPGzIU'
        with urllib.request.urlopen(url) as in_stream, open(f'sample2.jpg', 'wb') as out_file:
            copyfileobj(in_stream, out_file)

        request_photo = ImageFile(open('sample2.jpg', 'rb'))
        # Processing
        # give image to neural network
        # get image back from neural network

        # save response to database
        user_response = Response.objects.create(image=request_photo)
        user_response.save()
        # save request to database
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, zoom=zoom,
                                              image=request_photo,
                                              user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        if os.path.exists('sample2.jpg'):
            os.remove('sample2.jpg')

        return render(request, 'detection/result.html', {'user_request': user_request})
    else:
        return render(request, 'detection/detect.html', {})


def test(request):
    req = get_object_or_404(Request, id=20)
    return render(request, 'detection/test.html', {'req': req})
