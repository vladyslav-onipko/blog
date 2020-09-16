from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.fields import AutoSlugField

from utilities.utils import slug_generator, get_image_path


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    birthday = models.CharField(max_length=20, blank=True)
    slug = AutoSlugField(populate_from='full_name', slugify_function=slug_generator)
    photo = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return self.full_name
