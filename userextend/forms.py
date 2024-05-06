from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
import random

from django.core.exceptions import ValidationError
from django.forms import TextInput, Select, NumberInput, EmailInput
from home.models import SiteUser


class AuthenticationNewForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your password'})


class SiteUserForm(UserCreationForm):
    class Meta:
        model = SiteUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone_number',
            'city',
            'address',
        ]
        labels = {
            'username': 'Email',
        }

    # UserModelForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your first name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your last name'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your phone number'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Please enter your city'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your address'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your password confirmation'})


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if SiteUser.objects.filter(username=username).exists():
            self.add_error('username', 'Email already exists in database!')
        return username


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city']

        widgets = {
            'first_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter user's first name"}),
            'last_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter user's last name"}),
            'email': EmailInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter user's email"}),
            'phone_number': NumberInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter user's phone number"}),
            'address': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter user's address"}),
            'city': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter user's city"}),
        }


class PasswordResetForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please enter: Old Password'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please enter: New Password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Please confirm: New Password'}))

    class Meta:
        model = SiteUser
        fields = ['old_password', 'new_password1', 'new_password2']
