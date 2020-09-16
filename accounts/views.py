from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User

from utilities.utils import ObjectDeleteMixin, slug_generator

from blog.models import Post
from accounts.models import Profile
from accounts.forms import ProfileEditForm, RegistrationForm


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        is_taken = User.objects.filter(email=email).exists()
        if is_taken:
            data = {
                'is_taken': 'User with this email has already exist',
            }
            return JsonResponse(data)
        else:
            return super(RegistrationView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(slug=self.kwargs['slug'])
        return context


class ProfileEditView(FormView):
    template_name = 'registration/profile_edit_form.html'
    form_class = ProfileEditForm

    def get_initial(self):
        data = {
            'full_name': self.request.user.profile.full_name,
            'birthday': self.request.user.profile.birthday,
            'photo': self.request.user.profile.photo
        }
        self.initial = data
        return super(ProfileEditView, self).get_initial()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES, instance=request.user.profile)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = slug_generator(instance.user.username)
        form.save()
        return super(ProfileEditView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'slug': self.request.user.profile.slug})


class UserPostView(TemplateView):
    template_name = 'user_posts.html'

    def get_context_data(self, **kwargs):
        context = super(UserPostView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(user=self.request.user)
        return context


class DeletePostView(ObjectDeleteMixin, TemplateView):
    template_name = 'delete_user_post.html'
    context_name = 'post'
    model = Post
    redirect_url = 'user-posts'

