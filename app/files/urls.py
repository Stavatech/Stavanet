from django.urls import path
from . import views

urlpatterns = [
    path('', views.FileUpload.as_view()),
]
