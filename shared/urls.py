from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^get-csrf-token$', views.get_csrf_token),
	url(r'^get-full-url$', views.get_full_url)
]
