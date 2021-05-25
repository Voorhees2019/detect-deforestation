from django.shortcuts import render, get_object_or_404, redirect
from .models import Request, Response
import urllib.request
from shutil import copyfileobj
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
import os
import tensorflow as tf
import numpy as np
import cv2


model = tf.keras.models.load_model('./detection/model_main.h5')
counter = 1


@login_required
def detection(request):
    return render(request, 'detection/detect.html', {})


def handle_uploaded_file(uploaded_file):
    with open(f'{uploaded_file.name}', 'wb+') as destination_file:
        for chunk in uploaded_file.chunks():
            destination_file.write(chunk)


def detect(file_name):
    """ Processing image with neural network """
    base_name = file_name.rpartition(".")[0]
    # model = tf.keras.models.load_model('./detection/model_main.h5')

    # loss = model.evaluate(test_dataset, steps=test_steps)
    # print(loss)

    def read_image(path):
        x = cv2.imread(path, cv2.IMREAD_COLOR)
        x = cv2.resize(x, (512, 512))
        x = x / 256.0
        return x

    def mask_parse(mask):
        mask = np.squeeze(mask)
        mask = [mask, mask, mask]
        mask = np.transpose(mask, (1, 2, 0))
        return mask

    x = f'./{file_name}'
    x = read_image(x)
    y_pred = model.predict(np.expand_dims(x, axis=0))[0] > 0.5
    h, w, _ = x.shape
    all_images = [
        mask_parse(y_pred) * 256.0
    ]
    image = np.concatenate(all_images, axis=1)
    cv2.imwrite(f'./{base_name}_response.png', image)


@login_required
def detect_uploaded_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('uploaded_file')
        img_base_name = uploaded_file.name.rpartition(".")[0]
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        handle_uploaded_file(uploaded_file)

        # Processing image
        detect(uploaded_file.name)

        # save response to database
        user_response = Response.objects.create(image=ImageFile(open(f'./{img_base_name}_response.png', 'rb')))
        user_response.save()

        # save request to database
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, image=uploaded_file,
                                              user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        if os.path.exists(f'./{uploaded_file.name}'):
            os.remove(f'./{uploaded_file.name}')
        if os.path.exists(f'./{img_base_name}_response.png'):
            os.remove(f'./{img_base_name}_response.png')

        return redirect('query_detail', query_id=user_request.id)
    # GET
    else:
        return render(request, 'detection/detect.html', {})


@login_required
def detect_on_map(request):
    global counter
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        zoom = request.POST.get('zoom')

        url = f'https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size=640x640&maptype=satellite&key=AIzaSyDGHMwuICv6YA1GJvYS2tiodBVIgKPGzIU'
        with urllib.request.urlopen(url) as in_stream, open(f'map_query_{counter}.png', 'wb') as out_file:
            copyfileobj(in_stream, out_file)

        # Processing image
        detect(f'map_query_{counter}.png')

        # save response to database
        user_response = Response.objects.create(image=ImageFile(open(f'./map_query_{counter}_response.png', 'rb')))
        user_response.save()
        # save request to database
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, zoom=zoom,
                                              image=ImageFile(open(f'map_query_{counter}.png', 'rb')),
                                              user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        if os.path.exists(f'./map_query_{counter}.png'):
            os.remove(f'./map_query_{counter}.png')
        if os.path.exists(f'./map_query_{counter}_response.png'):
            os.remove(f'./map_query_{counter}_response.png')

        counter += 1
        return redirect('query_detail', query_id=user_request.id)
    # GET
    else:
        return render(request, 'detection/detect.html', {})


def query_detail(request, query_id):
    query_obj = get_object_or_404(Request, pk=query_id)
    return render(request, 'detection/query-detail.html', {'query': query_obj})


def query_delete(request, query_id):
    query_obj = get_object_or_404(Request, pk=query_id)
    query_obj.delete()
    return redirect('dashboard')


def latest_queries(request):
    queries = Request.objects.order_by('-date_uploaded')
    paginator = Paginator(queries, 10)
    page = request.GET.get('page')
    paged_queries = paginator.get_page(page)
    return render(request, 'detection/queries.html', {'queries': paged_queries})
