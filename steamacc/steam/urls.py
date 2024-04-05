from django.urls import path

from . import views

app_name = 'steam'

urlpatterns = [
    path('', views.index, name='index'),
]
