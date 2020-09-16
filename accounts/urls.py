from django.urls import path
from accounts import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='register'),
    path('profile/<slug:slug>', views.ProfileView.as_view(), name='profile'),
    path('<slug:slug>/edit', views.ProfileEditView.as_view(), name='profile-edit'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', PasswordChangeView.as_view(
        template_name='registration/password_change.html'), name='password-change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html')),

    path('posts/', views.UserPostView.as_view(), name='user-posts'),
    path('delete/<slug:slug>/', views.DeletePostView.as_view(), name='post-delete'),
]
