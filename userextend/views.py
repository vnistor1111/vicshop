from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from home.models import SiteUser
# from vic_shop.settings import EMAIL_HOST_USER
from userextend.forms import SiteUserForm, UserUpdateForm, PasswordResetForm


class UserCreateView(CreateView):
    template_name = 'userextend/create_user.html'
    model = User
    form_class = SiteUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.first_name = new_user.first_name.title()
        new_user.last_name = new_user.last_name.title()
        new_user.email = new_user.username
        new_user.save()

        return redirect('login')


class UserUpdateView(UpdateView):
    template_name = 'userextend/update_user.html'
    model = SiteUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('list-products')


class UserDeleteView(DeleteView):
    template_name = 'userextend/delete_user.html'
    model = SiteUser
    success_url = reverse_lazy('list-products')


class UserDetailView(DetailView):
    template_name = 'userextend/detail_user.html'
    model = SiteUser


class UserChangePasswordView(PasswordChangeView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('details_user')
    template_name = 'userextend/change_password.html'
    model = SiteUser

    def get_success_url(self):
        return reverse_lazy('details_user', kwargs={'pk': self.request.user.pk})

    def get_form_kwargs(self): # Provide the current user instance to the form
        kwargs = super().get_form_kwargs() # Call the base implementation first to get a dictionary of form keyword arguments
        kwargs['user'] = self.request.user # Add the 'user' key to the kwargs dictionary with the current user instance
        return kwargs # Return the updated kwargs dictionary



