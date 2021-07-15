from django.shortcuts import render


def index(request):
    """Home page of blog app."""
    return render(request, 'blog/index.html')
