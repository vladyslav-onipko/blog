from django.urls import path
from blog import views
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home-page'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post_new/', views.CreatePostView.as_view(), name='post-new'),
    path('post/<slug:slug>/edit', views.EditPostView.as_view(), name='post-edit'),
    path('rubric/<slug:slug>/', views.RubricDetailView.as_view(), name='rubric-detail'),
    path('tag/<slug:slug>', views.TaggedPostView.as_view(), name='posts-tagged'),
]

