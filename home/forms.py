from django import forms
from django.forms import TextInput, EmailInput, Select, NumberInput, Textarea

from home.models import Product, Category, ProductReview


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by']

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter product name"}),
            'category': Select(
                attrs={'class': 'form-select'}),
            'description': Textarea(
                attrs={'class': 'form-control', 'placeholder': "Please enter product description", 'rows': 10}),
            # You can change the number of rows as needed
            'price': NumberInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter product price (in RON)"}),
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter product name"}),
            'category': Select(
                attrs={'class': 'form-select'}),
            'description': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter product description"}),
            'price': NumberInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter product price"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'placeholder': "Please enter product category name"}),
            'slug': TextInput(
                attrs={'class': 'form-select', 'placeholder': "Please enter product category slug"})
        }


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['comment', 'rating', 'product']
        widgets = {
            'product': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your comment'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
