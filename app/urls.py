from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_page_view, name = 'home'),
    path('base', views.base_page_view, name = 'base'),
    path('register', views.register_page_view, name = 'register'),
    path('login', views.login_page_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path('category/<int:id>/', views.category_page_view, name = 'category'),
    path('product/<int:id>/', views.product_page_view, name='product'), 
    path('addCustomOrder/<int:id>/', views.add_custom_order_page_view, name='addCustomOrder'), 
    path('changeListStatus/<int:id>/', views.product_change_list_status_view, name='changeListStatus'), 
    path('addProduct', views.add_product_page_view, name = 'addProduct'),
    path('editProduct/<int:id>/', views.edit_product_page_view, name = 'editProduct'),
    path('removeProduct/<int:id>/', views.product_remove_view, name='removeProduct'), 
    path('userProfile', views.user_profile_view, name = 'userProfile'),
    path('userEdit', views.user_profile_edit_view, name = 'userEdit'),
    path('userDelete/<int:id>/', views.user_delete_view, name = 'userDelete'),
    path('changeBlockStatus/<int:id>/', views.user_change_block_status_view, name='changeBlockStatus'), 
    path('addWishList', views.add_wish_list_view, name = 'addWishList'),
]