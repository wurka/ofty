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
# from django.contrib import admin
from . import views

urlpatterns = [
	path('demo', views.demo),
	url(r'^add-new-unit$', views.add_new_unit, name='units/add-new-unit'),
	url(r'^add-new-unit-test$', views.add_new_unit_test),
	url(r'^get-groups$', views.get_groups),
	url(r'^get-group-parameters$', views.get_group_parameters),
	path('get-my-units', views.get_my_units, name='get-my-units'),
	path('get-all-units', views.get_all_units, name='get-all-units'),
	url(r'^ajax-test$', views.ajax_test),
	url(r'^color-picker-source$', views.color_picker_source),
	url(r'^materials-source$', views.materials_source),
	url(r'^delete-unit$', views.delete_unit),
	path('unit/<int:unit_id>', views.unit, name='units/unit'),
	path('publish', views.publish),
	path('unpublish', views.unpublish),
	path('update', views.update)
]
