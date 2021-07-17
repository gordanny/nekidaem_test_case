from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.views import View

from .models import Post, Subscribe, ReadedPosts


class Index(View):
    """Home page of blog app."""
    template = 'blog/index.html'

    def get(self, request):

        return render(request, self.template)


class Blog(View):
    template = 'blog/blog.html'

    def get(self, request, blogger):
        blogger = User.objects.get(username=blogger)
        posts = Post.objects.filter(author=blogger.id).order_by('-pub_date')[:20]
        homepage = blogger == request.user
        if homepage:
            subscribed = False
        else:
            is_subscribed = Subscribe.objects.filter(blogger_id=blogger.id, subscriber_id=request.user.id)
            subscribed = True if is_subscribed else False
        context = {'posts': posts, 'homepage': homepage, 'subscribed': subscribed}
        return render(request, self.template, context)

    def post(self, request, blogger):
        blogger = User.objects.get(username=blogger)
        is_subscribed = Subscribe.objects.filter(blogger_id=blogger.id, subscriber_id=request.user.id)
        if is_subscribed:
            is_subscribed.delete()
        else:
            s = Subscribe(blogger_id=blogger.id, subscriber_id=request.user.id)
            s.save()
        return self.get(request, blogger)


class BloggersList(View):
    template = 'blog/bloggers.html'

    def get(self, request):
        bloggers = User.objects.filter(is_superuser='f')
        context = {'bloggers': bloggers}
        return render(request, self.template, context)


class Feed(View):
    template = 'blog/feed.html'

    def get(self, request):
        subscriptions = Subscribe.objects.filter(subscriber_id=request.user.id)
        # Make an empty queryset.
        posts = Post.objects.filter(author=False)
        for subscription in subscriptions:
            subscription_posts = Post.objects.filter(author=subscription.blogger.id)[:20]
            posts = posts.union(subscription_posts).order_by('pub_date')
        context = {'posts': posts[:20]}
        return render(request, self.template, context)
