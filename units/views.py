from django.shortcuts import HttpResponse
from .models import Group
import json


# Create your views here.
def add_new_unit(request):
	return HttpResponse("OK")


def get_groups(request):
	if "parentid" in request.GET:  # запрашивается не корневой элемент
		try:
			pid = int(request.GET["parentid"])
		except ValueError:
			return HttpResponse("not valid parentid", status=500)
		try:
			parent = Group.objects.get(id=pid)
		except Group.DoesNotExist:
			return HttpResponse(f"there is no group with id {pid}")
		groups = Group.objects.filter(parent=parent)
		ans = list()
		for group in groups:
			ans.append({

			})
	return HttpResponse("")


def get_group_parameters(request):
	return HttpResponse("")


def get_my_units(request):
	return HttpResponse("")