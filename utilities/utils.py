from slugify import slugify
from django.http import HttpResponseRedirect
from django.urls import reverse
import string
import random


def string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def slug_generator(data):
    slug = slugify(data)
    new_slag = f'{slug}-{string_generator(size=3)}'
    return new_slag


def get_image_path(instance, filename):
    return f'{instance}/{filename}'


def image_path(self):
    pass


class ObjectDeleteMixin:
    template_name = None
    redirect_url = None
    model = None
    context_name = None

    def get(self, request, *args, **kwargs):
        return super(ObjectDeleteMixin, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ObjectDeleteMixin, self).get_context_data(**kwargs)
        context[self.context_name] = self.model.objects.get(slug=self.kwargs['slug'])
        return context

    def post(self, request, *args, **kwargs):
        obj = self.model.objects.get(slug=self.kwargs['slug'])
        obj.delete()
        return HttpResponseRedirect(reverse(self.redirect_url))
