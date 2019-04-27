from django.urls import path
from . import views

urlpatterns = [
    path('', views.FileList.as_view()),
    path(r'<str:id>', views.FileDownload.as_view()),
]
