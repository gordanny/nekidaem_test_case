from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Post


def index(request):
    """Home page of blog app."""
    return render(request, 'blog/index.html')


def blog(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user.id).order_by('-pub_date')
    context = {'posts': posts}
    return render(request, 'blog/blog.html', context)
