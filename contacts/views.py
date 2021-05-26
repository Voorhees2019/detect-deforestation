from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from detection.models import Request
from django.contrib import messages
from django.core.mail import send_mail
import os


def contact(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        if request_id:
            user_request = get_object_or_404(Request, id=request_id)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Check if user has made an inquiry already
        if request.user.is_authenticated and request_id:
            has_contacted = Contact.objects.filter(request=user_request, user=request.user)
            if has_contacted:
                messages.error(request, 'You have already informed us about this query')
                return redirect('dashboard')

        if request.user.is_authenticated:
            if request_id:
                contact = Contact(request=user_request, user=request.user, name=name, email=email, phone=phone,
                                  message=message)
            else:
                contact = Contact(user=request.user, name=name, email=email, phone=phone, message=message)
        else:
            contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()

        # Send email
        send_mail(
            'Query Issues',
            f'There has been an issue for some Request:"{message}". Sign into the admin panel for more info.',
            os.environ.get('EMAIL_USER'),
            ['petrikartur@gmail.com'],
            fail_silently=False
        )
        messages.success(request, 'Your request has been submitted, developer will get back to you soon')
    return redirect('dashboard')
