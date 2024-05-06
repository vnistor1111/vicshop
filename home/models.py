import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# User
class SiteUser(AbstractUser):
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.username

    # Category


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # cod unic de identificare atasat url-ului specific categoriei

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    # Product


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_by = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='static/home/products/')
    slug = models.SlugField(max_length=20, unique=True)  # cod unic de identificare atasat url-ului specific produsului
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)  # ordonam produsele incepand cu cel mai nou adaugat in bd

    def __str__(self):
        return self.name

    def is_favorite(self, user):
        return self.favorites.filter(user=user).exists()

    # Favorite Product


class Favorite(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    # Product Reviews


class ProductReview(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    comment = models.TextField()
    rating_choices = [(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]
    rating = models.PositiveIntegerField(choices=rating_choices, default=5)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'
        ordering = ['-created_on']

    def __str__(self):
        user_name = self.user.get_full_name() if self.user else "Anonymous"
        return 'Comment on {} by {}'.format(self.product, user_name)

    def get_rating(self):
        return self.rating

    # Contact


class Contact(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=11)

    def __str__(self):
        return self.subject


# Cart

class Cart(models.Model):
    STATUS = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='open')

    def get_total_price(self):
        return sum(item.quantity * item.product.price for item in self.cartitem_set.all())


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Order(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f'Order {self.order_id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
