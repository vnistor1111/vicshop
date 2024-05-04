# from django.contrib import admin
#
# from home.models import *
#
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active']
#
#
# admin.site.register(SiteUser, UserAdmin),
# admin.site.register(Category),
# admin.site.register(Product),
# admin.site.register(Contact),
# admin.site.register(ProductReview),
# admin.site.register(Cart),
# admin.site.register(CartItem),
# admin.site.register(Newsletter),
# admin.site.register(NewsletterSubscriber),
# admin.site.register(Favorite),

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from home.models import *


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    # Add the list_display to show the fields you want on the admin page
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active', 'group_list']

    # Add a method to retrieve the groups a user belongs to
    def group_list(self, user):
        return ', '.join(group.name for group in user.groups.all())

    # Add filter_horizontal to make it easier to add and remove groups
    filter_horizontal = ('groups', 'user_permissions',)


# Register the SiteUser with the new UserAdmin
admin.site.register(SiteUser, UserAdmin)

# Register the rest of your models
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(ProductReview)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)

