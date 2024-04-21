from django.shortcuts import render

from home.models import Category


def category_list_view(request):
    category_list = Category.objects.all()
    return {'category_list': category_list}
