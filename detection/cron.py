from django.core.mail import send_mail
from .views import detect, get_static_map_image, delete_excess_images
from accounts.models import Profile
from detection.models import Request
from PIL import Image
from django.core.files.images import ImageFile


def my_scheduled_job():
    for profile in Profile.objects.filter(send_updates=True):
        requests_to_check = Request.objects.filter(user=profile.user, check_weekly=True)
        for request in requests_to_check:
            lat = request.latitude
            lng = request.longitude
            zoom = request.zoom
            base_filename = f'{lat}_{lng}'

            # Request static image
            get_static_map_image(lat, lng, zoom, base_filename)
            # Process image
            detect(f'{base_filename}.png')

            # Compare responses
            img1 = Image.open(request.response.image.path)
            img2 = Image.open(f'./{base_filename}_response.png')

            if not list(img1.getdata()) == list(img2.getdata()):
                # Responses are Different
                response = request.response

                # Change current request and response images to new ones
                request.image = ImageFile(open(f'{base_filename}.png', 'rb'))
                request.save()
                response.image = ImageFile(open(f'./{base_filename}_response.png', 'rb'))
                response.save()

                # Send email
                send_mail(
                    'ALERT attention',
                    f'We have detected changes in forest condition since your last request at {lat}, {lng} '
                    f'coordinates ({request.date_uploaded}). Make sure it is not illegal deforestation.',
                    'nnewsteam2015@gmail.com',
                    [profile.user.email],
                    fail_silently=False
                )

            # Delete excess images
            delete_excess_images(base_filename)
