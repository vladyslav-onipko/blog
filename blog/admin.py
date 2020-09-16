from django.contrib import admin
from blog.models import Rubric, Post, Comment


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ('title', )


@admin.register(Post)
class RubricAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class RubricAdmin(admin.ModelAdmin):
    pass
