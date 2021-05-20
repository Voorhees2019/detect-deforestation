from django.urls import path
from . import views

urlpatterns = [
    path('', views.detect, name='detect'),
    path('response1/', views.detect_uploaded_file, name='detect_uploaded_file'),
    path('response2/', views.detect_on_map, name='detect_on_map'),
]
