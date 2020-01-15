"""ofty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from . import views
from . import sitemaps

urlpatterns = [
	path('csrf/', views.csrf),
	url(r'^admin/', admin.site.urls),
	url(r'^units/', include('units.urls')),
	url(r'^message/', include('message.urls')),
	url(r'^statistic/', views.statistic),
	url(r'^account/', include('account.urls')),
	url(r'^shared/', include('shared.urls')),
	path('orders/', include('orders.urls')),
	url(r'^$', views.index, name='index'),
	path(
		'sitemap.xml', sitemap, {'sitemaps': sitemaps.ofty_maps},
		name='django.contrib.sitemaps.views.sitemaps'),
	path('favicon.ico', RedirectView.as_view(url='/static/img/shared/favicon.ico'), name='favicon'),
	# пути для js файлов (frontend)
	path('office/account-settings', views.account_settings),
	path('office/calendar', views.not_implemented),
	path('office/orders', views.not_implemented),
	path('office/deals', views.not_implemented),
	path('office/unit-storage', views.unit_storage),
	path('office/shop', views.not_implemented),
	path('office/my-sets', views.not_implemented),
	path('unit-search', views.unit_search),
]
