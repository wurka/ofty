from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login$', views.login),
	url(r'^login-page$', views.login_page),
	url(r'^status$', views.login_info)
]