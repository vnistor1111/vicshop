from django.contrib import admin

from home.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active']


admin.site.register(SiteUser, UserAdmin),
admin.site.register(Category),
admin.site.register(Product),
admin.site.register(Contact),
admin.site.register(ProductReview),
admin.site.register(Cart),
admin.site.register(CartItem),
admin.site.register(Newsletter),
admin.site.register(NewsletterSubscriber)

