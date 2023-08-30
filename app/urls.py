from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_page_view, name = 'home'),
    path('base', views.base_page_view, name = 'base'),
    path('register', views.register_page_view, name = 'register'),
    path('login', views.login_page_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path('addProduct', views.add_product_page_view, name = 'addProduct'),
    path('category/<int:id>/', views.category_page_view, name = 'category'),
    path('product/<int:id>/', views.product_page_view, name='product'), 
    path('userProfile', views.user_profile_view, name = 'userProfile'),
    path('userEdit', views.user_profile_edit_view, name = 'userEdit'),
    path('addWishList', views.add_wish_list_view, name = 'addWishList'),
]