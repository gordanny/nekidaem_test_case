"""Defines URL patterns for blog."""

from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views


app_name = 'blog'

urlpatterns = [
    # App home page.
    path('', views.Index.as_view(), name='index'),
    # Enable default authentication URL.
    path('auth/', include('django.contrib.auth.urls')),
    # The blog page.
    path('<str:blogger>/', views.Blog.as_view(), name='blog'),
    # List of bloggers.
    path('bloggers', views.BloggersList.as_view(), name='bloggers'),
    # Feed with unread posts from subscriptions.
    path('feed', views.Feed.as_view(), name='feed'),
    # Add new post page.
    path('new_post', login_required(views.NewPost.as_view()), name='new_post'),
    # Edit post page.
    path('edit_post/<int:post_id>', login_required(views.EditPost.as_view()), name='edit_post'),
]
