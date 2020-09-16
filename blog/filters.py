import django_filters

from blog.models import Post


class PostFilter(django_filters.FilterSet):
    ORDERING = (
        ('new', 'Newest first'),
        ('old', 'Oldest first')
    )

    ordering = django_filters.ChoiceFilter(label='',
                                           choices=ORDERING,
                                           method='filter_by_date',
                                           initial='new',
                                           )

    class Meta:
        model = Post
        fields = ['ordering']

    def filter_by_date(self, queryset, name, value):
        sorting = 'pub_date' if value == 'old' else '-pub_date'
        return queryset.order_by(sorting)

