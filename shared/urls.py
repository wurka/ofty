from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^get-csrf-token', views.get_csrf_token)
]
