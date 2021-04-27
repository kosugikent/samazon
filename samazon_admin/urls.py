from django.urls import path

from samazon_admin import views

app_name = 'samazon_admin'
urlpatterns = [
    # viewsディレクトリの__init__.pyにfrom .home import *を記述しておくことで、views.HomeViewを参照することができる。
    path('', views.HomeView.as_view(), name='home'),

    path('major_categories/', views.MajorCategoryListView.as_view(), name='major_category_list'),
    path('major_categories/create/', views.MajorCategoryCreateView.as_view(), name='major_category_create'),
    path('major_categories/<int:pk>/', views.MajorCategoryDetailView.as_view(), name='major_category_detail'),
    path('major_categories/<int:pk>/update/', views.MajorCategoryUpdateView.as_view(), name='major_category_update'),
    path('major_categories/<int:pk>/delete/', views.MajorCategoryDeleteView.as_view(), name='major_category_delete'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/delete_revive', views.UserDeleteReviveView.as_view(), name='user_delete_revive'),
]
