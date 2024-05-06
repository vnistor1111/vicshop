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


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'date_joined', 'is_staff', 'is_active', 'group_list']

    def group_list(self, user):
        return ', '.join(group.name for group in user.groups.all())

    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(SiteUser, UserAdmin)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(ProductReview)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)
