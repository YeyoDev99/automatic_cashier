from django.urls import path, include
from . import views

app_name = 'cashier'

urlpatterns = [
    path("",views.index, name='index'),
    path("sign_up/", views.sign_up, name='sign_up'),
    path('card_activation/', views.card_activation, name='card_activation'),
    path('menu/', views.menu, name='menu'),
    path('logout/', views.logout_user, name='logout'),
    path('check_balance/', views.check_balance, name='check_balance'),
    path('card_validation/<int:trans>/<int:tries>/', views.card_validation, name='card_validation'),
    path('deposit_money/', views.deposit_money, name='deposit_money')
]
