from django.urls import path
from userextend import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view(), name='create_user'),
    path('update_user/', views.UserUpdateView.as_view(), name='update_user'),
    path('update_user/<int:pk>/', views.UserUpdateView.as_view(), name='update_user'),
    path('delete_user/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('details_user/<int:pk>/', views.UserDetailView.as_view(), name='details_user'),
    path('profile_reset_password/<int:pk>/', views.UserChangePasswordView.as_view(),
         name='profile_reset_password'), # user profile reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name="password_reset"),  # submit email view
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
         name="password_reset_done"),  # email sent success
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
         name="password_reset_confirm"), # link to password reset from mail
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_complete"),  # password successfully changed
]
