"""Defines URL patterns for blog."""

from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    # App home page.
    path('', views.index, name='index'),
    # Enable default authentication URL.
    path('auth/', include('django.contrib.auth.urls')),
    # The blog page.
    path('blogs/<str:username>', views.blog, name='blog'),
    # List of bloggers.
    path('bloggers', views.bloggers_list, name='bloggers'),
]
