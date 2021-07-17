from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text


class Subscribe(models.Model):
    blogger = models.ForeignKey(User, related_name='blogger', on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, related_name='subscriber', on_delete=models.CASCADE)


class ReadedPosts(models.Model):
    subscription = models.ForeignKey(Subscribe, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
