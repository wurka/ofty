from django.shortcuts import HttpResponse, render
from .models import Group, GroupParameter, Color, Unit, UnitColor
import json
import random
import os
from django.http import JsonResponse


# Create your views here.
def add_new_unit(request):
	#return HttpResponse('ttp')
	"""
	Добавление нового товара
	:param request:
	:return: ОК - если добавлено. status = 500 и текст ошибки, если не удалось добавить
	"""
	#return HttpResponse("ZHOPAA", status=501)
	must_be = [
		"weight", "bail", "count", "title", "first-day-cost", "rent-min-days", "day-cost",
		"rent-min-days", "day-cost", "unit-group", "unit-colors", "parameters"
	]
	must_be_files = ["photo1", "photo2", "photo3", "photo4", "photo5"]

	for mfile in must_be_files:
		if mfile in request.FILES:
			print(f"accepted file <{mfile}>")
			# return HttpResponse("There is no photo1 - photo5 files", status=500)

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

		param = "unit-group"
		unit_group = int(request.POST[param])

		param = "unit-colors"
		unit_colors = json.loads(request.POST[param])

		param = "parameters"
		unit_parameters = json.loads(request.POST[param])

		print("creating new unit...")

		new_unit = Unit()
		new_unit.weight = weight
		new_unit.bail = bail
		new_unit.count = count
		new_unit.title = title
		new_unit.first_day_cost = first_day_cost
		new_unit.rent_min_days = rent_min_days
		new_unit.day_cost = day_cost

		# проверка на то, что группа, которую предлагает пользователь - существует
		try:
			new_unit_group = Group.objects.get(id=unit_group)
		except Group.DoesNotExist:
			return HttpResponse(f"Unknown unit group ({unit_group})", status=500)

		# кроме того, добавлять можно ТОЛЬКО товары групп, которые не имеют потомков
		childs = Group.objects.filter(parent=new_unit_group)
		if len(childs) > 0:
			return HttpResponse("This group cann't be used to save unit", status=500)

		new_unit.group = new_unit_group
		new_unit.save()  # без сохранения нельзя ссылаться
		print(f"unit with id ({new_unit.id}) was sucessfully created")

		# проверка и сохранение цветов
		try:
			for color_id in unit_colors:
				color_check = Color.objects.get(id=color_id)
				UnitColor.objects.create(color=color_check, unit=new_unit)
		except Color.DoesNotExist:
			return HttpResponse("Wrong color id", status=500)

		# сохранение в файловый архив фотографий
		# TODO: добавить полноценную проверку на тип фотографии (PILLOW)
		folder = os.path.join("user_uploads", f"user_{0}", f"unit_{new_unit.id}")
		os.makedirs(folder, exist_ok=True)

		file_count = 0
		for file_name in must_be_files:
			if file_name in request.FILES:
				uploading = request.FILES[file_name]
				extension = uploading.name.split(".")[-1]
				destination = os.path.join(folder, f"{file_name}.{extension}")
				with open(destination, "wb+") as file2write:
					for chunk in uploading.chunks():
						file2write.write(chunk)
				file_count += 1
		if file_count == 0:
			return HttpResponse("Must be at least one photo file", status=500)

	except ValueError:
		return HttpResponse(f"Wrong value of parameter {param}", status=500)

	return HttpResponse("OK")


def add_new_unit_test(request):
	n = len(Group.objects.all())
	random_group = None

	if n > 0:
		# подбирает группу, у которой нет детей (последняя в дереве)
		rand_indx = random.randint(0, n-1)
		steps = 0
		while random_group is None and steps < n:
			random_group = Group.objects.all()[(rand_indx + steps) % n]
			bads = Group.objects.filter(parent=random_group)
			if len(bads) > 0:
				random_group = None
			steps += 1

		params = GroupParameter.objects.filter(owner=random_group) if random_group is not None else list()
		json_params = {
			param.name: f"{random.randint(0, 100500)}" for param in params
		}
		json_params = json.dumps(json_params)
	else:
		json_params = "[]"

	random_colors = list()
	for i in range(random.randint(1, 5)):
		nc = len(Color.objects.all())
		if nc > 0:
			new_color = Color.objects.all()[random.randint(0, nc-1)]
			if new_color not in random_colors:
				random_colors.append(new_color)
	json_colors = json.dumps(random_colors)

	pars = {
		"json_params": json_params,
		"json_colors": json_colors,
		"random_group": random_group
	}

	return render(request, "units/unit-new-unit-test.html", pars)


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
				"picture": request.build_absolute_uri("/static/img/grouppreview/" + group.picture),
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
	my_units = Unit.objects.all()
	ans = list()
	for unit in my_units:
		appended_unit = {
			'id': unit.id,
			'weight': unit.weight,
			'bail': unit.bail,
			'count': unit.count,
			'title': unit.title,
			'first_day_coust': unit.first_day_cost,
			'rent_min_days': unit.rent_min_days,
			'day_cost': unit.day_cost,
			'group': unit.group.id,
		}
		# цвета
		aunit_colors = UnitColor.objects.filter(unit=unit)
		appended_unit['colors'] = [
			{
				#'id': c.color.id,
				#'color_group': c.color.color_group,
				#'rgb_hex': c.color.rgb_hex,
				#'texture': c.color.texture
			} for c in aunit_colors]

		# список фотографий (возможно, стоит сделать заполнение базы нормальное. это может быть быстрее, чем
		# поиск по файловой системе наличия файла и решит проблемы со списком форматов)
		for i in range(1, 6):
			userid = 0  # !!!!! TODO: получать id активного пользователя
			img_formats = ['jpg', 'jpeg', 'png']
			for img_format in img_formats:
				photo_path = os.path.join(
					os.getcwd(), 'user_uploads', f'user_{userid}', f'unit_{unit.id}', f'photo{i}.{img_format}')
				if os.path.exists(photo_path):
					appended_unit[f'photo{i}'] = request.build_absolute_uri(
						f'/static/user_{userid}/unit_{unit.id}/photo{i}.{img_format}')
					break
		ans.append(appended_unit)

	return JsonResponse(ans, safe=False)


def ajax_test(request):
	return render(request, "units/ajax-test.html")


