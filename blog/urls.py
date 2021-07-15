"""Defines URL patterns for blog."""

from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    # Enable default authentication URL.
    path('auth/', include('django.contrib.auth.urls')),
]
