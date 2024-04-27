from home.models import Category
from home.views import get_open_cart


def category_list_view(request):
    category_list = Category.objects.all()
    return {'category_list': category_list}


def cart_item_count(request):
    if request.user.is_authenticated:
        cart = get_open_cart(request)
    else:
        cart = None
    item_count = cart.cartitem_set.count() if cart is not None else 0
    return {'cart_item_count': item_count}
