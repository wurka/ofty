from django.urls import path
from . import views


urlpatterns = [
    path('get-content', views.get_content, name='basket-get-content'),
    path('add-unit', views.add_unit, name='basket-add-unit'),
    path('remove-unit', views.remove_unit, name='basket-remove-unit'),
]
