from django.urls import path
from . import views

urlpatterns = [
    path('', views.detect, name='detect'),
    path('result1/', views.detect_uploaded_file, name='detect_uploaded_file'),
    path('result2/', views.detect_on_map, name='detect_on_map'),
    path('test/', views.test, name='test'),
]
