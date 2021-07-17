from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.views import View

from .models import Post, Subscribe, ReadedPosts
from .forms import PostForm


class Index(View):
    """Home page of blog app."""
    template = 'blog/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:feed')
        else:
            return render(request, self.template)


class Blog(View):
    template = 'blog/blog.html'

    def get(self, request, blogger):
        blogger = get_object_or_404(User, username=blogger)
        posts = Post.objects.filter(author=blogger.id).order_by('-pub_date')[:20]
        subscribe_check = Subscribe.objects.filter(blogger_id=blogger.id, subscriber_id=request.user.id)
        is_subscribed = True if subscribe_check else False
        context = {'posts': posts, 'is_subscribed': is_subscribed, 'blogger': blogger}
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
            posts = posts.union(subscription_posts).order_by('-pub_date')
        context = {'posts': posts[:20]}
        return render(request, self.template, context)

    def post(self, request, post_id):
        pass


class NewPost(View):
    template = 'blog/new_post.html'

    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, self.template, context)

    def post(self, request):
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog:blog', blogger=request.user)
        context = {'form': form}
        return render(request, self.template, context)


class EditPost(View):
    template = 'blog/edit_post.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=post)
        context = {'post': post, 'form': form}
        return render(request, self.template, context)

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:blog', blogger=request.user)
        context = {'post': post, 'form': form}
        return render(request, self.template, context)
