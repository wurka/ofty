from django.shortcuts import render
from units.models import Group, Unit
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import HttpResponse


def statistic(request):
	params = {
		"count_users": len(User.objects.all()),
		"count_unit_types": len(Group.objects.all()),
		"count_units": len(Unit.objects.all())
	}
	return render(request, "ofty/statistic.html", params)


def index(request):
	return render(request, "ofty/index.html")


def csrf(request):
	ans = get_token(request)
	return HttpResponse(ans)


def unit_search(request):
	return render(request, 'ofty/unit-search.html')


def unit_storage(request):
	return render(request, 'ofty/unit-storage.html')


def account_settings(request):
	return render(request, 'ofty/account-settings.html')


def unit_search(request):
	return render(request, 'ofty/unit-search.html')


def not_implemented(request):
	return HttpResponse("not implemented yet", status=501)
