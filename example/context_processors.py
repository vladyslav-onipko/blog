from blog.models import Post, Rubric


def extra_context(request, **kwargs):
    context = {}
    viewed = request.session.get('viewed', [])
    context['viewed'] = Post.objects.filter(slug__in=viewed).order_by('pub_date')
    context['rubrics'] = Rubric.objects.all()
    return context

