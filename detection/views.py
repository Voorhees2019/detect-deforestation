from django.shortcuts import render, get_object_or_404, redirect
from .models import Request, Response
import urllib.request
from shutil import copyfileobj
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
import cv2

# model = tf.keras.models.load_model('./detection/model_main.h5')
model = tf.keras.models.load_model(
    r'/home/voorhees/Documents/Python_Projects/detection_deforestation_project/detection/model_main.h5')


@login_required
def detection(request):
    return render(request, 'detection/detect.html', {})


def handle_uploaded_file(uploaded_file):
    """ Saving uploaded file to local storage """
    with open(f'{uploaded_file.name}', 'wb+') as destination_file:
        for chunk in uploaded_file.chunks():
            destination_file.write(chunk)


def get_static_map_image(latitude, longitude, zoom, base_filename):
    """ Requesting static image from Google static API """
    url = f'https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size=640x640&maptype=satellite&key=AIzaSyDGHMwuICv6YA1GJvYS2tiodBVIgKPGzIU'
    with urllib.request.urlopen(url) as in_stream, open(f'{base_filename}.png', 'wb') as out_file:
        copyfileobj(in_stream, out_file)


def detect(file_name):
    """ Processing image with neural network (detecting deforestation) """
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
    image = cv2.resize(mask_parse(y_pred) * 256.0, (640, 640))
    cv2.imwrite(f'./{base_name}_response.png', image)


def delete_excess_images(base_filename):
    """ Deleting excess uploaded and processed files locally after inserting into database """
    if os.path.exists(f'./{base_filename}.png'):
        os.remove(f'./{base_filename}.png')
    if os.path.exists(f'./{base_filename}_response.png'):
        os.remove(f'./{base_filename}_response.png')


@login_required
def detect_uploaded_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('uploaded_file')
        img_name = uploaded_file.name
        img_base_name = img_name.rpartition(".")[0]
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        check_weekly = True if 'check_weekly' in request.POST else False

        handle_uploaded_file(uploaded_file)

        # Processing image
        detect(img_name)

        # save response to database
        user_response = Response.objects.create(image=ImageFile(open(f'./{img_base_name}_response.png', 'rb')))
        user_response.save()

        # save request to database
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, image=uploaded_file,
                                              check_weekly=check_weekly, user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        if os.path.exists(f'./{img_name}'):
            os.remove(f'./{img_name}')
        if os.path.exists(f'./{img_base_name}_response.png'):
            os.remove(f'./{img_base_name}_response.png')

        return redirect('query_detail', query_id=user_request.id)
    # GET
    else:
        return render(request, 'detection/detect.html', {})


@login_required
def detect_on_map(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        zoom = request.POST.get('zoom')
        check_weekly = True if 'check_weekly' in request.POST else False
        base_filename = f'{latitude}_{longitude}'

        # Request static image
        get_static_map_image(latitude, longitude, zoom, base_filename)

        # Process image
        detect(f'{base_filename}.png')

        # save response to database
        user_response = Response.objects.create(image=ImageFile(open(f'./{base_filename}_response.png', 'rb')))
        user_response.save()
        # save request to database
        user_request = Request.objects.create(latitude=latitude, longitude=longitude, zoom=zoom,
                                              image=ImageFile(open(f'{base_filename}.png', 'rb')),
                                              check_weekly=check_weekly, user=request.user, response=user_response)
        user_request.save()

        # Delete excess images
        delete_excess_images(base_filename)

        return redirect('query_detail', query_id=user_request.id)
    # GET method
    else:
        return render(request, 'detection/detect.html', {})


def query_detail(request, query_id):
    query_obj = get_object_or_404(Request, pk=query_id)
    return render(request, 'detection/query-detail.html', {'query': query_obj})


def query_delete(request, query_id):
    query_obj = get_object_or_404(Request, pk=query_id)
    if query_obj.user == request.user:
        query_obj.delete()
    return redirect('dashboard')


def latest_queries(request):
    queries = Request.objects.order_by('-date_uploaded')
    paginator = Paginator(queries, 10)
    page = request.GET.get('page')
    paged_queries = paginator.get_page(page)
    return render(request, 'detection/queries.html', {'queries': paged_queries})
