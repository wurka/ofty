from django.shortcuts import HttpResponse, render
from .models import Group, GroupParameter
import json


# Create your views here.
def add_new_unit(request):
	return HttpResponse("OK")


def get_groups(request):
	ans = list()
	if "parentid" in request.GET:  # запрашивается не корневой элемент
		try:
			pid = int(request.GET["parentid"])
		except ValueError:
			return HttpResponse("not valid parentid", status=500)
		try:
			parent = Group.objects.get(id=pid)
		except Group.DoesNotExist:
			return HttpResponse(f"there is no group with id {pid}", status=500)
		groups = Group.objects.filter(parent=parent)
	else:  # не указан родитель - отдать <root>
		groups = Group.objects.filter(parent=None)

	for group in groups:
		ans.append({
			"id": group.id,
			"name": group.name
		})

	ans = json.dumps(ans)
	return HttpResponse(ans)


def get_group_parameters(request):
	if "groupid" not in request.GET:
		return HttpResponse("no groupid specified", status=500)
	else:
		try:
			gid = int(request.GET["groupid"])
			group = Group.objects.get(id=gid)
			pars = GroupParameter.objects.filter(owner=group)
			parameters = [{
				"id": p.id,
				"name": p.name,
				"dimension": p.dimension
			} for p in pars]

			ans = {
				"picture": "/static/img/group-picture/" + group.picture,
				"parameters": json.dumps(parameters)
			}
			return HttpResponse(json.dumps(ans))
		except ValueError:
			return HttpResponse("wrong groupid value", status=500)
		except Group.DoesNotExist:
			return HttpResponse(f"there is no group with id {gid}", status=500)
		except GroupParameter.DoesNotExist:
			return HttpResponse("some extract error", status=500)

def get_my_units(request):
	return HttpResponse("")


def ajax_test(request):
	return render(request, "units/ajax-test.html")
