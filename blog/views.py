from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Subquery
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
            subscribe = Subscribe(blogger_id=blogger.id, subscriber_id=request.user.id)
            subscribe.save()
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
            readed_posts = ReadedPosts.objects.filter(subscription_id=subscription.id)
            subscription_posts = Post.objects.filter(author=subscription.blogger.id).order_by('-pub_date')
            unreaded_posts = subscription_posts.exclude(id__in=Subquery(readed_posts.values('post_id')))[:20]
            posts = posts.union(unreaded_posts).order_by('-pub_date')
        context = {'posts': posts[:20]}
        return render(request, self.template, context)

    def post(self, request):
        post_id = request.POST['post_id']
        print(post_id)
        post = get_object_or_404(Post, id=post_id)
        subscription = Subscribe.objects.filter(blogger_id=post.author.id, subscriber_id=request.user.id)
        readed_post = ReadedPosts(post_id=post_id, subscription_id=subscription[0].id)
        readed_post.save()
        return self.get(request)


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
