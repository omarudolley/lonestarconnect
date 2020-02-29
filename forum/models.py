from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.utils.html import mark_safe


class Forum(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(thread__forum = self).count()

    def get_last_post(self):
        return Post.objects.filter(thread__forum= self).order_by('-created_at').first()


class Thread(models.Model):
    title = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(Forum,on_delete = models.CASCADE,related_name='thread')
    starter = models.ForeignKey(User, on_delete = models.CASCADE,related_name='thread')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_posts_count(self):
        return Post.objects.filter(thread= self).count()


class Post(models.Model):
    message = models.TextField(max_length=4000)
    thread = models.ForeignKey(Thread, on_delete = models.CASCADE,related_name = 'post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,related_name='post')
    updated_by = models.ForeignKey(User, on_delete = models.CASCADE,  null=True,related_name='+')

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
    def __str__(self):
        return self.message
