from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.db.models import F

from taggit.models import Tag

from utilities.utils import slug_generator
from blog.forms import PostForm, CommentForm, SearchForm
from blog.models import Post, Comment, Rubric
from blog.filters import PostFilter


class HomePageView(ListView):
    template_name = 'home_page.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        search_value = self.request.GET.get('search')
        if search_value:
            queryset = Post.objects.filter(title__icontains=search_value)
        else:
            queryset = PostFilter(self.request.GET, queryset=Post.objects.all()).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['filter_form'] = PostFilter
        context['search_form'] = SearchForm
        return context


class TaggedPostView(TemplateView):
    template_name = 'tagged_posts.html'
    
    def get_context_data(self, **kwargs):
        context = super(TaggedPostView, self).get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        context['posts'] = Post.objects.filter(tags=tag)
        return context


class RubricDetailView(DetailView):
    model = Rubric
    template_name = 'rubric_detail.html'

    context_object_name = 'rubric'

    def get_context_data(self, **kwargs):
        context = super(RubricDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(rubric=self.object)
        return context


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    form_class = CommentForm
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.slug})

    def get(self, request, *args, **kwargs):
        viewed = request.session.get('viewed', [])
        post = Post.objects.get(slug=self.kwargs['slug'])
        Post.objects.filter(slug=post.slug).update(views=F('views') + 1)
        if post not in viewed:
            if len(viewed) == 3:
                viewed.pop()
            viewed.append(post.slug)
        request.session['viewed'] = viewed
        return super(PostDetailView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-pub_date')[:5]
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.post = self.object
        instance.save()
        return super(PostDetailView, self).form_valid(form)


class CreatePostView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'post_create_form.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user-posts')


class EditPostView(UpdateView):
    model = Post
    template_name = 'post_edit_form.html'
    form_class = PostForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.slug = slug_generator(instance.title)
        instance.save()
        return super(EditPostView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user-posts')
