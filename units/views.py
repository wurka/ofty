from django.shortcuts import HttpResponse, render
from .models import Group, GroupParameter, Color, Unit, UnitColor, UnitParameter
from .models import Material, UnitMaterial, Set, SetElement, Keyword, UnitKeyword
import json
import random
import os
from datetime import datetime
from django.http import JsonResponse


# Create your views here.
def add_new_unit(request):
	"""
	Добавление нового товара
	:param request:
	:return: ОК - если добавлено. status = 500 и текст ошибки, если не удалось добавить
	"""
	must_be = [
		"weight", "bail", "count", "title", "first-day-cost", "rent-min-days", "day-cost",
		"unit-group", "unit-colors", "parameters",
		"unit-materials", "sets", "keywords", "description"
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

		param = "unit-materials"
		unit_materials = json.loads(request.POST[param])

		param = "sets"
		unit_sets = json.loads(request.POST[param])

		param = "keywords"
		unit_keywords = request.POST[param].split()

		param = "description"
		description = request.POST[param]

		print("creating new unit...")

		new_unit = Unit()
		new_unit.weight = weight
		new_unit.bail = bail
		new_unit.count = count
		new_unit.title = title
		new_unit.first_day_cost = first_day_cost
		new_unit.rent_min_days = rent_min_days
		new_unit.day_cost = day_cost
		new_unit.description = description

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

		new_unit.save()  # без сохранения невозможно сделать ссылку на него

		# валидация и сохранения UnitParameters
		if type(unit_parameters) is not dict:
			param = "parameters"
			raise ValueError()
		base_params = GroupParameter.objects.filter(owner=new_unit.group)
		for base_param in base_params:
			mykey = str(base_param.id)
			if mykey not in unit_parameters:
				return HttpResponse(f"There is no parameter with id {mykey} in unit_parameters", status=500)
			new_unit_param = UnitParameter(
				value=unit_parameters[mykey],  # вот она синхронизация ввода и базы
				parameter=base_param,
				unit=new_unit
			)
			new_unit_param.save()

		# валидация и сохранения UnitMaterials
		if type(unit_materials) is not list:
			param = "unit-materials"
			raise ValueError()
		for material_id in unit_materials:
			base_material = Material.objects.get(id=material_id)
			new_unit_material = UnitMaterial(
				unit=new_unit,
				material=base_material
			)
			new_unit_material.save()

		# валидация и сохранения Sets
		if type(unit_sets) is not list:
			param = "sets"
			raise ValueError()
		for set_id in unit_sets:
			base_set = Set.objects.get(id=set_id, is_deleted=False)
			new_unit_set = SetElement(
				unit=new_unit,
				set=base_set
			)
			new_unit_set.save()

		# keywords
		if type(unit_sets) is not list:
			param = "sets"
			raise ValueError()
		for keyword in unit_keywords:
			keyword = keyword.lower()
			try:
				base_keywrd = Keyword.objects.get(name=keyword)
				new_unit_keyword = UnitKeyword(
					unit=new_unit,
					keyword=base_keywrd,
					creation_time=datetime.now()
				)
				new_unit_keyword.save()
			except Keyword.DoesNotExist:  # такого ключа ещё нет в базе
				new_keyword = Keyword.objects.create(
					name=keyword,
					creation_time=datetime.now()
				)
				new_unit_keyword = UnitKeyword(
					unit=new_unit,
					keyword=new_keyword,
					creation_time=datetime.now()
				)
				new_unit_keyword.save()

	except ValueError:
		return HttpResponse(f"Wrong value of parameter {param}", status=500)
	except Material.DoesNotExist:
		return HttpResponse("Seems like specified material does not exists", status=500)

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
	my_units = Unit.objects.filter(is_deleted=False)
	ans = list()
	for unit in my_units:
		appended_unit = {
			'id': unit.id,
			'weight': unit.weight,
			'bail': unit.bail,
			'count': unit.count,
			'title': unit.title,
			'first_day_cost': unit.first_day_cost,
			'rent_min_days': unit.rent_min_days,
			'day_cost': unit.day_cost,
			'group': unit.group.id,
			'commentary': unit.description,
		}
		# параметры (соответствующие группе)
		unit_parameters = UnitParameter.objects.filter(unit=unit)
		appended_unit['parameters'] = [
			{
				'id': p.parameter.id,
				'name': p.parameter.name,
				'value': p.value,
				'dimension': p.parameter.dimension
			} for p in unit_parameters
		]

		# материалы
		unit_materials = UnitMaterial.objects.filter(unit=unit)
		appended_unit['materials'] = [
			{
				'id': m.material.id,
				'name': m.material.name
			} for m in unit_materials
		]

		# наборы (sets)
		unit_sets = SetElement.objects.filter(unit=unit)
		appended_unit['sets'] = [
			{
				'id': s.set.id,
				'name': s.set.title
			} for s in unit_sets if s not in appended_unit['sets']
		]

		# keywords (теги)
		unit_keywords = UnitKeyword.objects.filter(unit=unit)
		appended_unit['keywords'] = [
			{
				'id': k.keyword.id,
				'word': k.keyword.name
			} for k in unit_keywords
		]

		# цвета
		aunit_colors = UnitColor.objects.filter(unit=unit)
		appended_unit['colors'] = [
			{
				'id': c.color.id,
				'color_group': c.color.color_group,
				'rgb_hex': c.color.rgb_hex,
				'texture': c.color.texture
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


def color_picker_source(request):
	ans = dict()

	for group in [f"group{i+1}" for i in range(5)]:
		ans[group] = {
			group: [{
				'id': c.id,
				'rgb_hex': c.rgb_hex,
				'texture': request.build_absolute_uri("/static/img/units/texture/" + c.texture)
			}] for c in Color.objects.filter(color_group=group)
		}

	return JsonResponse(ans)


def delete_unit(request):
	if 'id' not in request.POST:
		return HttpResponse("There is no id in POST request", status=500)
	try:
		uid = int(request.POST['id'])
		to_del_unit = Unit.objects.get(id=uid, is_deleted=False)
		to_del_unit.is_deleted = True
		to_del_unit.save()
	except ValueError:
		return HttpResponse("Wrong value of id parameter: {}".format(request.POST['id']), status=500)
	except Unit.DoesNotExist:
		return HttpResponse(f"There is no Unit with id {uid}", status=500)

	return HttpResponse("OK")
