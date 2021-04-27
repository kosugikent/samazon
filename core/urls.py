from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('categories/<int:pk>/products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/review/', views.ProductReviewView.as_view(), name='product_review'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/<int:pk>/update/', views.CartUpdateView.as_view(), name='cart_update'),
    path('cart/delete/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('favorite/', views.FavoriteView.as_view(), name='favorite'),
    path('favorite/add/', views.FavoriteAddDeleteView.as_view(), name='favorite_add_delete'),
    path('favorite/delete/', views.FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('mypage/profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('mypage/credit_card/create', views.CreditCardCreateView.as_view(), name='credit_card_create'),
    path('mypage/address/update/', views.AddressUpdateView.as_view(), name='address_update'),
    path('mypage/user/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('payment/', views.PaymentView.as_view(), name='payment')
]
