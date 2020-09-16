from django import forms

from ckeditor.widgets import CKEditorWidget

from blog.models import Post, Comment, Rubric


class PostForm(forms.ModelForm):
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(),
                                    empty_label=None
                                    )
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter post title'}))
    content = forms.CharField(widget=CKEditorWidget)

    class Meta:
        model = Post
        exclude = ('user', 'slug', 'pub_date', 'change_date', 'views')


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea(attrs={'placeholder': 'Enter your comment'}))

    class Meta:
        model = Comment
        exclude = ('user', 'post')


class SearchForm(forms.Form):
    search = forms.CharField(required=False,
                             widget=forms.TextInput(attrs={'placeholder': 'Search'})
                             )