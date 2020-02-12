from django.urls import path
from . import views


urlpatterns = [
    path('get-my-orders', views.get_my_orders, {'mode': 'order'}, name='get-my-orders'),
    path('get-my-deals', views.get_my_orders, {'mode': 'deal'}, name='get-my-deals'),
    path('new-order', views.new_order, name='new-order'),
]
