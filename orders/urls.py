from django.urls import path
from . import views


urlpatterns = [
    path('get-my-orders', views.get_my_orders, name='get-my-orders'),
]
