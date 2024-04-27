from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, DetailView

import secret
from .filters import ProductFilter
from .forms import ProductForm, CategoryForm, ProductReviewForm, ContactForm
from .models import Product, Category, ProductReview, Cart, CartItem


class HomeTemplateView(TemplateView):
    template_name = 'home/index.html'


class AboutUsTemplateView(TemplateView):
    template_name = 'home/about_us.html'


class ContactFormView(TemplateView):
    template_name = 'home/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save()

            send_mail(
                'New Contact Submission',
                f"Subject: {new_contact.subject}\nMessage: {new_contact.message}\nEmail: {new_contact.email}\nPhone: {new_contact.phone_number}",
                secret.email_user,
                [secret.email_user],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to a 'thank you' page or back to the contact form
    else:
        form = ContactForm()

    return render(request, 'home/contact.html', {'form': form})


class ProductListView(ListView):
    template_name = 'product/list_of_products.html'
    model = Product
    context_object_name = 'all_products'
    paginate_by = 50

    def get_queryset(self):
        products = Product.objects.all()
        prod_filter = ProductFilter(self.request.GET, queryset=products)
        return prod_filter.qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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


class ProductReviewUpdateView(UpdateView):
    template_name = 'product/update_review.html'
    form_class = ProductReviewForm
    model = ProductReview
    success_url = reverse_lazy('detail-products')

    def get_success_url(self):
        return reverse_lazy('product-details', kwargs={
            'pk': self.object.product.pk})  # foloseste primary key al produsului din instanta product_review


class ProductReviewDeleteView(DeleteView):
    template_name = 'product/delete_review.html'
    model = ProductReview
    success_url = reverse_lazy('detail-products')

    def get_success_url(self):
        product_review = self.get_object()
        return reverse_lazy('product-details', kwargs={'pk': product_review.product.pk})


@login_required
def cart_view(request):
    cart = get_open_cart(request)
    cart_items = cart.cartitem_set.all()
    total_price = 0
    if cart_items:
        total_price = cart.get_total_price()
    else:
        messages.info(request, 'Your cart is empty.')
    return render(request, 'product/cart.html', {'cart': cart, 'total_price': total_price, 'cart_items': cart_items})


@login_required
def get_open_cart(request):
    user = request.user
    open_cart, created = Cart.objects.get_or_create(status='open', user=user)
    return open_cart


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        if 'product_id' in request.POST:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))
            cart = get_open_cart(request)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
            cart_item.quantity += quantity
            if cart_item.quantity > 0:
                cart_item.save()
            else:
                cart_item.delete()
            messages.success(request, 'Item added to cart successfully.')

    return redirect(request.META.get('HTTP_REFERER', reverse_lazy('cart')))
