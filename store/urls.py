from django.urls import path
from .views import home, about, login_user, logout_user, user_register, product, category, categories_summary, \
    user_update, password_update, info_update, search_items

app_name = 'store'

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('user-register/', user_register, name='user_register'),
    path('user-update/', user_update, name='user_update'),
    path('info-update/', info_update, name='info_update'),
    path('password-update/', password_update, name='password_update'),
    path('product/<int:pk>/', product, name='product'),
    path('category/<slug:slug>/', category, name='category'),
    path('categories_summary/', categories_summary, name='categories_summary'),
    path('search/', search_items, name='search')

]