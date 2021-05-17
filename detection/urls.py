from django.urls import path
from . import views

urlpatterns = [
    path('', views.detect, name='detect'),
    path('result1/', views.detect_uploaded_file, name='detect_uploaded_file'),
]
