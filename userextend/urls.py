from django.urls import path

from userextend import views
from userextend.forms import AuthenticationNewForm

urlpatterns = [
    path('create_user/', views.UserCreateView.as_view(), name='create_user'),
    path('update_user/', views.UserUpdateView.as_view(), name='update_user'),
    path('update_user/<int:pk>/', views.UserUpdateView.as_view(), name='update_user'),
    path('delete_user/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('details_user/<int:pk>/', views.UserDetailView.as_view(), name='details_user'),
    path('reset_password/<int:pk>/', views.UserChangePasswordView.as_view(), name='reset_password'),
    # path('user_history/', views.UserHistoryView.as_view(), name='user_history'),
]

