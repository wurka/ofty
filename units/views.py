from django.shortcuts import HttpResponse, render
from .models import Group, GroupParameter, Color, Unit, UnitColor, UnitParameter
from .models import Material, UnitMaterial, Set, SetElement, Keyword, UnitKeyword
import json
import random
import os
from datetime import datetime
from django.http import JsonResponse
from django.contrib.sitemaps import Sitemap
import sys
from shared.methods import get_with_parameters, post_with_parameters
from .models import UnitPhoto
from io import BytesIO
from PIL import Image


def demo(request):
	pars = {
		"username": "Anonymous" if request.user.is_anonymous else request.user.username,
		"userid": "X" if request.user.is_anonymous else request.user.id
	}
	return render(request, 'units/demo.html', pars)


def logged(method):
	def inner(request):
		if request.user.is_anonymous:
			return HttpResponse("you must be loggined in", status=401)
		return method(request)
	return inner


def validate_int(where, key, min_val, max_val):
	if key not in where:
		raise ValueError(f"{key} not found")
	try:
		val = int(where[key])
	except ValueError:
		raise ValueError(f"{where[key]} not valid integer")
	if val < min_val or val > max_val:
		raise ValueError(f'{key} must be {min_val} to {max_val}, but {val} given')
	return val


def validate_json(where, key):
	if key not in where:
		raise ValueError(f"{key} not found")
	try:
		val = json.loads(where[key])
	except json.JSONDecodeError as e:
		raise ValueError(f'{key} not valid json object: ' + str(e))
	return val


def validate_float(where, key, min_val, max_val):
	if key not in where:
		raise ValueError(f"{key} not found")
	try:
		val = float(where[key])
	except ValueError:
		raise ValueError(f"{where[key]} not valid float")
	if val < min_val or val > max_val:
		raise ValueError(f'{key} must be {min_val} to {max_val}, but {val} given')
	return val


def validate_string(where, key, max_length):
	if key not in where:
		raise ValueError(f"{key} not found")
	val = str(where[key])
	if len(val) > max_length:
		raise ValueError(f'max length for {key} ({max_length}) exceeded')
	return val


def validate_bool(where, key):
	if key not in where:
		raise ValueError(f"{key} not found")
	if type(where[key]) is bool:
		return where[key]
	elif type(where[key]) is str:
		if where[key].lower() == "true":
			return True
		elif where[key].lower() == "false":
			return False
		else:
			raise ValueError(f'{key}: {where[key]} can not be interpreted as bool')
	else:
		raise ValueError(f'{key}: type not supported: {type(where[key])}')


# Create your views here.
@logged
@post_with_parameters(
	"weight", "bail", "count", "title", "first-day-cost", "rent-min-days", "day-cost",
	"unit-group", "unit-colors", "parameters",
	"unit-materials", "sets", "keywords", "description", "published")
def add_new_unit(request):
	"""
	Добавление нового товара
	:param request:
	:return: ОК - если добавлено. status = 500 и текст ошибки, если не удалось добавить
	"""
	must_be_files = ["photo1", "photo2", "photo3", "photo4", "photo5"]

	for mfile in must_be_files:
		if mfile in request.FILES:
			print(f"accepted file <{mfile}>")
			# return HttpResponse("There is no photo1 - photo5 files", status=500)

	try:
		weight = validate_float(request.POST, 'weight', 0.001, 10_000)
		bail = validate_float(request.POST, "bail", 0, 1_000_000)
		count = validate_int(request.POST, 'count', 1, 1_000_000)

		setid = validate_int(request.POST, 'set', 0, sys.maxsize) if 'set' in request.POST else 0
		title = validate_string(request.POST, 'title', 50)

		first_day_cost = validate_float(request.POST, 'first-day-cost', 0, 1_000_000)
		rent_min_days = validate_int(request.POST, "rent-min-days", 1, 5_000)
		day_cost = validate_float(request.POST, "day-cost", 1, 1_000_000)

		unit_group = validate_int(request.POST, "unit-group", 1, sys.maxsize)
		unit_colors = validate_json(request.POST, "unit-colors")
		unit_parameters = validate_json(request.POST, "parameters")
		unit_materials = validate_json(request.POST, "unit-materials")
		unit_sets = validate_json(request.POST, "sets")
		unit_keywords = request.POST["keywords"].split()
		description = request.POST["description"]

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
		new_unit.owner = request.user
		new_unit.published = validate_bool(request.POST, "published")

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
		folder = os.path.join("user_uploads", f"user_{request.user.id}", f"unit_{new_unit.id}")
		os.makedirs(folder, exist_ok=True)

		file_count = 0
		for file_name in must_be_files:
			if file_name in request.FILES:
				uploading = request.FILES[file_name]
				extension = uploading.name.split(".")[-1]
				# чтение в память (для обработки)
				buffer = BytesIO()
				for chunk in uploading.chunks():
					buffer.write(chunk)
				# обработка изображения
				buffer.seek(0)
				image = Image.open(buffer)
				width, height = image.size
				size = min(width, height)
				image = image.crop((width/2 - size/2, height/2 - size/2, width/2 + size/2, height/2 + size/2))
				image = image.resize((186, 186), Image.BILINEAR)

				# запись на диск
				destination = os.path.join(folder, f"{file_name}.{'jpeg'}")
				image.save(destination, format='JPEG')

				# with open(destination, "wb+") as file2write:
				# for chunk in uploading.chunks():
				# file2write.write(chunk)

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
		if type(unit_keywords) is not list:
			param = "keywords"
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

		new_unit.build_search_string()  # сгенерировать строку для поиска

	except ValueError as e:
		return HttpResponse(f"error in parameter: {str(e)}", status=500)
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
			"name": group.name,
			"group-image": request.build_absolute_uri("/static/img/grouppreview/" + group.picture),
		})

	ans = json.dumps(ans)
	return HttpResponse(ans)


@get_with_parameters("groupid")
def get_group_parameters(request):
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


def units_to_json(request, units, build_headers=False, last_id=0):
	# преобразовать list<Unit> в json
	# request нужен для построения absolute_url
	ans = list()
	for unit1 in units:
		if build_headers:
			if unit1.group.id != last_id:  # предыдущая группа была не такой, как эта
				group = unit1.group
				groups = list()
				# формирование списка заголовков
				while group is not None:
					groups.insert(0, group)  # Нужен обратный порядок
					group = group.parent

				level = 1
				for g in groups:
					ans.append({
						"type": f"header{level}",
						"text": g.name
					})
					level += 1

				last_id = unit1.group.id

		appended_unit = {
			'type': 'unit',
			'id': unit1.id,
			'weight': unit1.weight,
			'bail': unit1.bail,
			'count': unit1.count,
			'title': unit1.title,
			'first-day-cost': unit1.first_day_cost,
			'rent-min-days': unit1.rent_min_days,
			'day-cost': unit1.day_cost,
			'unit-group': unit1.group.id,
			'description': unit1.description,
			'published': unit1.published,
			'owner': unit1.owner.id
		}
		# параметры (соответствующие группе)
		unit_parameters = UnitParameter.objects.filter(unit=unit1)
		appended_unit['parameters'] = [
			{
				'id': p.parameter.id,
				'name': p.parameter.name,
				'value': p.value,
				'dimension': p.parameter.dimension
			} for p in unit_parameters
		]

		# материалы
		unit_materials = UnitMaterial.objects.filter(unit=unit1)
		appended_unit['unit-materials'] = [
			{
				'id': m.material.id,
				'name': m.material.name
			} for m in unit_materials
		]

		# наборы (sets)
		unit_sets = SetElement.objects.filter(unit=unit1)
		appended_unit['sets'] = [
			{
				'id': s.set.id,
				'name': s.set.title
			} for s in unit_sets if s not in appended_unit['sets']
		]

		# keywords (теги)
		unit_keywords = UnitKeyword.objects.filter(unit=unit1)
		appended_unit['keywords-info'] = [
			{
				'id': k.keyword.id,
				'word': k.keyword.name
			} for k in unit_keywords
		]

		appended_unit['keywords'] = " ".join([u.keyword.name for u in unit_keywords])

		# цвета
		aunit_colors = UnitColor.objects.filter(unit=unit1)
		appended_unit['unit-colors'] = [
			{
				'id': c.color.id,
				# 'color_group': c.color.color_group,
				'rgb_hex': c.color.rgb_hex,
				'texture': c.color.texture_url(request)
			} for c in aunit_colors]

		# информация о группах
		unit_groups = [unit1.group]
		parent = unit1.group.parent
		while parent:
			unit_groups.insert(0, parent)
			parent = parent.parent
		appended_unit["group-info"] = {
			"groups": json.dumps([g.name for g in unit_groups]),
			"group-image": request.build_absolute_uri("/static/img/grouppreview/" + unit1.group.picture),
			"params": [{
				"id": up.parameter.id,
				"name": up.parameter.name,
				"dimension": up.parameter.dimension,
				"value": up.value
			} for up in UnitParameter.objects.filter(unit=unit1)]
		}

		# список фотографий (возможно, стоит сделать заполнение базы нормальное. это может быть быстрее, чем
		# поиск по файловой системе наличия файла и решит проблемы со списком форматов)
		for i, photo in enumerate(UnitPhoto.get_unit_photos(unit1, request)):
			appended_unit[f'photo{i+1}'] = request.build_absolute_uri(photo)

		ans.append(appended_unit)
	return ans


@logged
def get_my_units(request):
	last_id = 0
	if "offset" in request.GET and "size" in request.GET and "filter" in request.GET:
		try:
			offset = int(request.GET["offset"])
			size = int(request.GET["size"])
			filtration = request.GET["filter"].lower()
			my_units = Unit.objects.filter(is_deleted=False, owner=request.user)
			my_units = my_units.filter(search_string__icontains=filtration).order_by('group__name')
			my_units = my_units[offset: offset + size]

			if "last-group-id" in request.GET:
				try:
					last_id = int(request.GET["last-group-id"])
				except ValueError:
					return HttpResponse("last-group-id parameter must be integer", status=500)

		except ValueError:
			return HttpResponse("offset and size must be integers", status=500)
	else:
		my_units = Unit.objects.filter(is_deleted=False, owner=request.user).order_by('group__name')

	ans = units_to_json(request, my_units, build_headers=True, last_id=last_id)

	return JsonResponse(ans, safe=False)


@get_with_parameters()
def get_all_units(request):
	units = Unit.objects.filter(published=True, is_deleted=False)
	ans = units_to_json(request, units)
	return JsonResponse(ans, safe=False)


def ajax_test(request):
	return render(request, "units/ajax-test.html")


def color_picker_source(request):
	ans = dict()

	for group in [f"group{i+1}" for i in range(5)]:
		ans[group] = [
			{
				'id': c.id,
				'rgb_hex': c.rgb_hex,
				'texture': c.texture_url(request)
			} for c in Color.objects.filter(color_group=group)
		]

	return JsonResponse(ans)


def materials_source(request):
	ans = [{
		'id': x.id,
		'name': x.name
	} for x in Material.objects.all()]
	return JsonResponse(ans, safe=False)


@logged
@post_with_parameters("id")
def delete_unit(request):
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


class TestMap(Sitemap):
	def items(self):
		return {'a': 'b'}


def get_sitemap(request):
	return Sitemap(request, {'test': TestMap})


def unit(request, unit_id):
	return HttpResponse(f"<div>there is unit with id: {unit_id}</div>")


# декораторы не нужны, т.к. функция не доступна через URL
def do_publish_unpublish(request, target):
	try:
		unit_one = Unit.objects.get(id=int(request.POST["id"]))
		unit_one.published = target
		unit_one.save()
	except ValueError:
		return HttpResponse(f"not valid id: {request.POST['id']}", status=500)
	except Unit.DoesNotExist:
		return HttpResponse(f'there is no unit with id {request.POST["id"]}', status=500)
	return HttpResponse("OK")


@logged
@post_with_parameters("id")
def publish(request):
	return do_publish_unpublish(request, True)


@logged
@post_with_parameters("id")
def unpublish(request):
	return do_publish_unpublish(request, False)


@logged
@post_with_parameters(
	"id", "weight", "bail", "count", "title", "first-day-cost", "rent-min-days", "day-cost",
	# "unit-group",  # группу нельзя менять
	"unit-colors", "parameters",
	"unit-materials", "keywords", "description", "published")
def update(request):
	try:
		uid = int(request.POST["id"])
		unit_one = Unit.objects.get(id=uid)
	except ValueError:
		return HttpResponse(f"id must be integer, not: {request.POST['id']}", status=500)
	except Unit.DoesNotExist:
		return HttpResponse(f"there is no unit with id {request.POST['id']}", status=500)

	try:
		unit_one.weight = float(request.POST["weight"])
		unit_one.bail = float(request.POST["bail"])
		unit_one.count = int(request.POST["count"])
		unit_one.title = request.POST["title"]
		unit_one.first_day_cost = float(request.POST["first-day-cost"])
		unit_one.rent_min_days = int(request.POST["rent-min-days"])
		unit_one.day_cost = float(request.POST["day-cost"])
		unit_one.description = request.POST["description"]
		unit_one.published = json.loads(request.POST["published"])

		base_params = GroupParameter.objects.filter(owner=unit_one.group)

		# сохранение параметров группы
		unit_parameters = json.loads(request.POST["parameters"])
		if type(unit_parameters) is not dict:
			raise json.JSONDecodeError("parameters must be list")
		for base_param in base_params:
			mykey = str(base_param.id)
			if mykey not in unit_parameters:
				return HttpResponse(f"There is no parameter with id {mykey} in unit_parameters", status=500)

			unit_param = UnitParameter.objects.get(unit=unit_one, parameter=base_param)
			unit_param.value = unit_parameters[mykey]
			unit_param.save()

		# проверка и сохранение цветов
		unit_colors = request.POST["unit-colors"]
		unit_colors = json.loads(unit_colors)
		if type(unit_colors) is not list:
			raise json.JSONDecodeError("unit-colors must be list")
		try:
			UnitColor.objects.filter(unit=unit_one).delete()  # удаляем старые цвета
			for color_id in unit_colors:
				color_id = int(color_id)
				color_check = Color.objects.get(id=color_id)
				UnitColor.objects.create(color=color_check, unit=unit_one)
		except Color.DoesNotExist:
			return HttpResponse("Wrong color id", status=500)

		# валидация и сохранения UnitMaterials
		unit_materials = json.loads(request.POST["unit-materials"])
		if type(unit_materials) is not list:
			raise ValueError("unit-materials must be list")
		UnitMaterial.objects.filter(unit=unit_one).delete()
		for material_id in unit_materials:
			base_material = Material.objects.get(id=material_id)
			new_unit_material = UnitMaterial(
				unit=unit_one,
				material=base_material
			)
			new_unit_material.save()

		# keywords
		unit_keywords = filter(None, request.POST["keywords"].split(" "))
		UnitKeyword.objects.filter(unit=unit_one).delete()  # удаление старых ключевых слов
		for keyword in list(unit_keywords):
			keyword = keyword.lower().strip()
			try:
				base_keywrd = Keyword.objects.get(name=keyword)
				new_unit_keyword = UnitKeyword(
					unit=unit_one,
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
					unit=unit_one,
					keyword=new_keyword,
					creation_time=datetime.now()
				)
				new_unit_keyword.save()

		unit_one.build_search_string()  # сгенерировать строку для поиска
	except ValueError as e:
		return HttpResponse("wrong parameter value: " + str(e), status=500)
	except KeyError as e:
		return HttpResponse("wrong object structure: " + str(e), status=500)

	return HttpResponse("OK")
