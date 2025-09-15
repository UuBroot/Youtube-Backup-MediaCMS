from django.urls import path
from . import views

urlpatterns = [
   path('', views.import_youtube, name='import_youtube'),
]

