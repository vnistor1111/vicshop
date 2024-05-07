from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from home.models import SiteUser
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

        # Adăugarea utilizatorului în grupul implicit
        my_group = Group.objects.get(name='customer')
        my_group.user_set.add(new_user)

        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'userextend/update_user.html'
    model = SiteUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('list-products')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'userextend/delete_user.html'
    model = SiteUser
    success_url = reverse_lazy('list-products')


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'userextend/detail_user.html'
    model = SiteUser


class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('details_user')
    template_name = 'userextend/change_password.html'
    model = SiteUser

    def get_success_url(self):
        return reverse_lazy('details_user', kwargs={'pk': self.request.user.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



