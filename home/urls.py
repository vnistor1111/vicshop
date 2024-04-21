from django.urls import path, include
from home import views
from home.views import ProductReviewView

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home_page'),
    path('list_products/', views.ProductListView.as_view(), name='list-products'),
    path('create_product/', views.ProductCreateView.as_view(), name='create-product'),
    path('update_product/<int:pk>/', views.ProductUpdateView.as_view(), name='update-product'),
    path('delete_product/<int:pk>/', views.ProductDeleteView.as_view(), name='delete-product'),
    path('product_details/<int:pk>/', views.ProductDetailView.as_view(), name='product-specifications'),
    path('create_category/', views.CategoryCreateView.as_view(), name='create-category'),
    path('category/<str:category_slug>/', views.product_category_search, name='product_category_search'),
    path('product_review/', ProductReviewView.as_view(), name='product_review')
]

