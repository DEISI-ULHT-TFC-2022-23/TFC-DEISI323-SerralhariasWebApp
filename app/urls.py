from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_page_view, name = 'home'),
    path('base', views.base_page_view, name = 'base'),
    path('register', views.register_page_view, name = 'register'),
    path('login', views.login_page_view, name = 'login'),
    path('addProduct', views.add_product_page_view, name = 'addProduct'),
    path('category/<str:category>/', views.category_page_view, name = 'category'),
    path('product/<int:id>/', views.product_page_view, name='product'), 
]