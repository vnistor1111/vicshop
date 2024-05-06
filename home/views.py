from math import floor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView, DetailView
import secret
from .filters import ProductFilter
from .forms import ProductForm, CategoryForm, ProductReviewForm, ContactForm, ConfirmationForm
from .models import Product, Category, ProductReview, Cart, CartItem, Favorite, Order, OrderItem


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
        all_products = self.get_queryset().annotate(average_rating=Avg('reviews__rating'))

        filter_params = self.request.GET.urlencode()

        for product in all_products:
            rating = product.average_rating or 0
            product.full_stars = floor(rating)
            product.half_star = rating % 1 >= 0.5
            product.favorite = False  # Default to False for all users
            product.add_favorite_url = f"{reverse('add_favorite', args=[product.id])}?{filter_params}"
            product.remove_favorite_url = f"{reverse('remove_favorite', args=[product.id])}?{filter_params}"

            # Format the average rating to two decimal places as a string
            if product.average_rating:
                product.formatted_average_rating = "{:.2f}".format(product.average_rating)
            else:
                product.formatted_average_rating = "No reviews yet"

        if self.request.user.is_authenticated:
            for p in all_products:
                p.favorite = p.is_favorite(self.request.user)

        data['all_products'] = all_products
        data['filters'] = ProductFilter(self.request.GET, queryset=self.get_queryset()).form
        return data


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'product/create_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('list-products')
    permission_required = 'home.add_product'

    def form_valid(self, form):
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = self.request.user
            product.save()
            return redirect(self.success_url)
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'product/update_product.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('list-products')
    permission_required = 'home.change_product'


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'product/delete_product.html'
    model = Product
    success_url = reverse_lazy('list-products')
    permission_required = 'home.delete_product'


class ProductDetailView(DetailView):
    template_name = 'product/product_details.html'
    model = Product


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'product/create_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('list-products')
    permission_required = 'home.add_category'


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'product/update_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('manage_categories')
    permission_required = 'home.change_category'


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'product/delete_category.html'
    model = Category
    success_url = reverse_lazy('manage_categories')
    permission_required = 'home.delete_category'


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    filter_params = request.GET.urlencode()
    return HttpResponseRedirect(f"{reverse('list-products')}?{filter_params}")
    # return redirect('list-products')  # Redirect to the product list page


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    filter_params = request.GET.urlencode()
    return HttpResponseRedirect(f"{reverse('list-products')}?{filter_params}")
    # return redirect('list-products')


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'product/list_of_favorites.html'
    context_object_name = 'list_of_favorites'

    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user).select_related('product').annotate(
            average_rating=Avg('product__reviews__rating'))
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        favorites = list(self.get_queryset())

        for favorite in favorites:
            if favorite.average_rating is not None:
                formatted_rating = "{:.2f}".format(favorite.average_rating)
            else:
                formatted_rating = None

            favorite.product.formatted_average_rating = formatted_rating
            favorite.product.full_stars = floor(favorite.average_rating or 0)
            favorite.product.half_star = (favorite.average_rating or 0) % 1 >= 0.5
            favorite.product.favorite = True
            favorite.product.has_reviews = favorite.product.reviews.exists()

        data['list_of_favorites'] = favorites
        return data


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'product/manage_category.html'
    model = Category
    context_object_name = 'all_categories'
    paginate_by = 50
    permission_required = 'home.view_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_products = {}
        for category in context['all_categories']:
            category_products[category.id] = category.products.filter(is_active=True)
        context['category_products'] = category_products
        return context


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


class ProductReviewUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'product/update_review.html'
    form_class = ProductReviewForm
    model = ProductReview
    success_url = reverse_lazy('detail-products')

    def get_success_url(self):
        return reverse_lazy('product-details', kwargs={
            'pk': self.object.product.pk})  # foloseste primary key al produsului din instanta product_review


class ProductReviewDeleteView(LoginRequiredMixin, DeleteView):
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


@login_required
def update_cart_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_change = int(request.POST.get('quantity_change'))
        cart = get_open_cart(request)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity += quantity_change
        if cart_item.quantity > 0:
            cart_item.save()
        else:
            cart_item.delete()
        messages.success(request, 'Cart updated successfully.')
    return redirect('cart')


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = get_open_cart(request)
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        messages.info(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def clear_cart(request):
    if request.method == 'POST':
        cart = get_open_cart(request)
        cart.cartitem_set.all().delete()
        messages.info(request, 'All items have been removed from your cart.')
    return redirect('cart')


class FAQ(TemplateView):
    template_name = 'home/faq.html'


def send_checkout_email(order, cart_items, cleaned_data, total_price):
    product_lines = []
    for item in cart_items:
        product_line = f"{item.product.name} - Quantity: {item.quantity}, Price per item: {item.product.price}"
        product_lines.append(product_line)

    product_details = "\n".join(product_lines)
    user_contact_details = (
        f"Name: {cleaned_data['first_name']} {cleaned_data['last_name']}\n"
        f"Email: {cleaned_data['email']}\n"
        f"Phone: {cleaned_data['phone_number']}\n"
        f"Address: {cleaned_data['address']}, {cleaned_data['city']}\n"
    )

    email_body = (
        "Thank you for your purchase!\n\n"
        "Here are the details of your order:\n"
        f"{product_details}\n\n"
        f"Total Price: {total_price} RON\n\n"
        "Your contact details for this order:\n"
        f"{user_contact_details}\n\n"
        "Payment is due by cash or card on delivery.\n\n"
        "If you have any questions or need to make changes to your order, please contact us immediately."
    )

    email_subject = f'Your Purchase Confirmation - Order ID: {order.order_id}'
    send_mail(
        email_subject,
        email_body,
        'from@example.com',  # Replace with your actual email
        [cleaned_data['email']],
        fail_silently=False,
    )



@login_required
def checkout(request):
    cart = get_open_cart(request)
    user = request.user
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'city': user.city,
        'address': user.address,
        'email': user.email,
        'phone_number': user.phone_number
    }

    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                cleaned_data = form.cleaned_data
                order = Order.objects.create(user=user)
                cart_items = cart.cartitem_set.all()
                total_price = cart.get_total_price()

                try:
                    for item in cart_items:
                        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity,
                                                 price=item.product.price)
                except Exception as e:
                    # Log the error or send it to an admin email
                    print(f"Error creating OrderItem: {e}")
                    # Optionally, you could also rollback the transaction
                    raise

                cart.status = 'closed'
                cart.save()
                cart.cartitem_set.all().delete()

                send_checkout_email(order, cart_items, cleaned_data, total_price)

                messages.success(request, 'Thank you for your purchase!')
                return redirect('thank_you')
    else:
        form = ConfirmationForm(initial=initial_data)

    context = {
        'form': form,
        'cart': cart,
        'user': user,
        'initial_data': initial_data
    }
    return render(request, 'product/checkout.html', context)


@login_required
def thank_you(request):
    return render(request, 'product/thank_you.html')
