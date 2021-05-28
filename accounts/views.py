from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from detection.models import Request
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html', {})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'Your account has been created successfully')
                    # login after registration
                    auth.login(request, user)
                    return redirect('dashboard')
        else:
            messages.error(request, 'Passwords did not match')
            return redirect('register')
    return render(request, 'accounts/register.html', {})


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        send_updates = True if 'send_updates' in request.POST else False

        # Change profile info
        user_obj = request.user
        user_obj.username = username
        user_obj.email = email
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.profile.send_updates = send_updates
        user_obj.save()
        return redirect('dashboard')
    # GET method
    return render(request, 'accounts/edit_profile.html', {})


@login_required
def dashboard(request):
    user_requests = Request.objects.filter(user=request.user).order_by('-date_uploaded')
    request_amount = user_requests.count()
    paginator = Paginator(user_requests, 10)
    page = request.GET.get('page')
    paged_user_requests = paginator.get_page(page)

    return render(request, 'accounts/dashboard.html', {'request_amount': request_amount,
                                                       'user_requests': paged_user_requests})
