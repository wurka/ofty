from django.shortcuts import HttpResponse, render
from .models import Group, GroupParameter
import json


# Create your views here.
def add_new_unit(request):
	"""
	Добавление нового товара
	:param request:
	:return: ОК - если добавлено. status = 500 и текст ошибки, если не удалось добавить
	"""
	Вес, кг: weight
	Залог, руб: bail
	Количество, шт: count
	Коллекция: set - id
	Название: title
	Первый
	день: first - day - cost
	Аренда
	от, дней: rent - min - days
	Аренда
	р / сут: day - cost
	Тип
	товара: unit - type
	Массив
	id
	цветов: unit - colors
	id
	группы: goupid
	список
	параметров: [{"id": id1, "value": val1}, {"id": id2, "value": val2}]
	must_be = [
		"weight", "bail", "count", "title", "first-day-cost", "rent-min-days", "day-cost",
	    "rent-min-days" , "day-cost", "unit-type", "unit-colors", "parameters"
	]

	for m in must_be:
		if m not in request.POST:
			return HttpResponse(f"There is no parameter {m} in POST request", status=500)

	try:
		param = "weight"
		weight = float(request.POST[param])
		param = "bail"
		bail = float(request.POST[param])
		param = "count"
		count = int(request.POST[param])

		param = "set"
		setid = int(request.POST[param]) if param in request.POST else 0

		param = "title"
		title = request.POST[param]

		param = "first-day-cost"
		first_day_cost = float(request.POST[param])

		param = "rent-min-days"
		rent_min_days = float(request.POST[param])

		param = "day-cost"
		day_cost = float(request.POST[param])

		param = "unit-type"
		unit_type = int(request.POST[param])

		param = "unit-colors"
		unit_colors = json.loads(param)

		param = "parameters"
		unit_parameters = json.loads(param)


	except ValueError:
		return HttpResponse(f"Wrong value of parameter {param}")

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
