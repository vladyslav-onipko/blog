from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from taggit.managers import TaggableManager
from django_extensions.db.fields import AutoSlugField

from utilities.utils import slug_generator, get_image_path


class Rubric(models.Model):
    title = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='title', slugify_function=slug_generator)

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateField(auto_now=True)
    slug = AutoSlugField(populate_from='title', slugify_function=slug_generator)
    tags = TaggableManager(blank=True)
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - timedelta(days=1))
