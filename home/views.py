from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, DetailView
from .filters import ProductFilter
from .forms import ProductForm, CategoryForm, ProductReviewForm
from .models import Product, Category, ProductReview
from django.contrib.auth.views import LoginView


class HomeTemplateView(TemplateView):
    template_name = 'home/index.html'


class ProductListView(ListView):
    template_name = 'product/list_of_products.html'
    model = Product
    context_object_name = 'all_products'

    # permission_required = 'product.view_list_of_products'

    def get_queryset(self):
        products = Product.objects.all()
        prod_filter = ProductFilter(self.request.GET, queryset=products)
        return prod_filter.qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # print(data)
        data['filters'] = ProductFilter(self.request.GET, queryset=self.get_queryset()).form
        return data


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'product/create_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('list-products')

    def form_valid(self, form):
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = self.request.user
            product.save()
            return redirect(self.success_url)
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    template_name = 'product/update_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('list-products')


class ProductDeleteView(DeleteView):
    template_name = 'product/delete_product.html'
    model = Product
    success_url = reverse_lazy('list-products')


class ProductDetailView(DetailView):
    template_name = 'product/product_details.html'
    model = Product


def review_detail(request, pk):
    review = get_object_or_404(ProductReview, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})


class CategoryCreateView(CreateView):
    template_name = 'product/create_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('list-products')


def product_category_search(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.GET:
        product_filter = ProductFilter(request.GET, queryset=Product.objects.filter(category=category))
    else:
        product_filter = ProductFilter(queryset=Product.objects.filter(category=category))

    return render(request, 'product/list_of_products.html', {'filter': product_filter})


class ProductReviewView(CreateView):
    form_class = ProductReviewForm
    template_name = 'product/product_review.html'
    model = ProductReview
    success_url = reverse_lazy('list-products')

    def get_initial(self):
        product_id = self.request.GET.get('product_id', Product.objects.first().id)
        return {'product': product_id}

    def form_valid(self, form):
        if form.is_valid():
            review = form.save(commit=False)
            review.user = self.request.user
            review.save()
            return redirect(self.success_url)
        return super().form_valid(form)
