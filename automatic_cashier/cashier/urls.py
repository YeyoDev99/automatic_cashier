from django.urls import path, include
from . import views

app_name = 'cashier'

urlpatterns = [
    path("index/",views.index, name='index')
]
