"""Defines URL patterns for blog."""

from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    # App home page.
    path('', views.Index.as_view(), name='index'),
    # Enable default authentication URL.
    path('auth/', include('django.contrib.auth.urls')),
    # The blog page.
    path('blogs/<str:blogger>', views.Blog.as_view(), name='blog'),
    # List of bloggers.
    path('bloggers', views.BloggersList.as_view(), name='bloggers'),
]
