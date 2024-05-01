from django.urls import path, include
from home import views
from home.views import ProductReviewView, contact, add_to_favorites, remove_from_favorites

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home_page'),
    path('about_us/', views.AboutUsTemplateView.as_view(), name='about_us'),
    path('contact/', contact, name='contact'),
    path('manage_categories/', views.CategoryListView.as_view(), name='manage_categories'),
    path('list_products/', views.ProductListView.as_view(), name='list-products'),
    path('create_product/', views.ProductCreateView.as_view(), name='create-product'),
    path('update_product/<int:pk>/', views.ProductUpdateView.as_view(), name='update-product'),
    path('delete_product/<int:pk>/', views.ProductDeleteView.as_view(), name='delete-product'),
    path('product_details/<int:pk>/', views.ProductDetailView.as_view(), name='product-details'),
    path('create_category/', views.CategoryCreateView.as_view(), name='create-category'),
    path('update_category/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('delete_category/<int:pk>/', views.CategoryDeleteView.as_view(), name='delete-category'),
    path('category/<str:category_slug>/', views.product_category_search, name='product_category_search'),
    path('product_review/', ProductReviewView.as_view(), name='product_review'),
    path('update_review/<int:pk>', views.ProductReviewUpdateView.as_view(), name='update-review'),
    path('delete_review/<int:pk>', views.ProductReviewDeleteView.as_view(), name='delete-review'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add_favorite/<int:product_id>/', add_to_favorites, name='add_favorite'),
    path('remove_favorite/<int:product_id>/', remove_from_favorites, name='remove_favorite'),
]


