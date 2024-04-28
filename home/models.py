from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# User
class SiteUser(AbstractUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    # email = models.EmailField(unique=True, null=False, blank=False)
    # username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)

    # date_joined = models.DateTimeField(auto_now_add=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    # Category


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # cod unic de identificare atasat url-ului specific categoriei

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    # Product


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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


class NewsletterSubscriber(models.Model):
    email = models.EmailField()


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    send_datetime = models.DateTimeField(default=timezone.now)


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




