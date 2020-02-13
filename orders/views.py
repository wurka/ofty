from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Order, OrderUnit
from shared.methods import logged, get_with_parameters, post_with_parameters
from units.models import UnitPhoto
from units.models import Unit
import json
from datetime import datetime, timedelta
import itertools


# Create your views here.
@logged
@get_with_parameters("page")
def get_my_orders(request, *args, **kwargs):
	mode = kwargs['mode']
	if mode == "order":
		orders = Order.objects.filter(client=request.user).order_by("id")
	elif mode == "deal":
		orders = Order.objects.filter(owner=request.user).order_by("id")
	photos = list()
	for order in orders:
		for ou in OrderUnit.objects.filter(order=order):
			try:
				photos.extend(UnitPhoto.get_unit_photos(ou.unit, request))
			except Unit.DoesNotExist:
				photos.append(request.build_absolute_uri("/static/img/shared/no_img.png"))

	ans = [{
		'id': order.id,
		"status": order.status,
		"statusText": Order.get_status_text(order.status),
		"start": f"{order.start_date.day:02}.{order.start_date.month:02}.{order.start_date.year}",
		"stop": f"{order.stop_date.day:02}.{order.stop_date.month:02}.{order.stop_date.year}",
		"commentary": order.commentary,
		"cost": order.cost,
		"bail": order.bail,
		"pictures": order.get_photos(request),
		"owner": order.owner_info(),
		"client": order.client_info(),
	} for order in orders]

	return JsonResponse(ans, safe=False)


@logged
@post_with_parameters("owner", "commentary", "start-date", "stop-date", "bail", "cost", "units")
def new_order(request):
	def dict_of_units(source, name):
		try:
			u_array = json.loads(source[name])

			if not type(u_array) is list:
				raise ValueError(f"{name} parameter must be a list")

			# в каждом объекте должны быть поля id, count
			if not all([
				type(x) is dict and
				"id" in x and
				"count" in x and
				type(x['count']) is int for x in u_array]):

				raise ValueError("wrong unit object structure")

			return u_array

		except json.decoder.JSONDecodeError:
			raise ValueError(f'{name} not valid json object')

	try:
		units = dict_of_units(request.POST, "units")
	except ValueError as e:
		return HttpResponse(str(e), status=500)

	def get_date(text):
		# format of text: YYYY.MM.DD
		words = text.split(".")
		date = datetime(int(words[2]), int(words[1]), int(words[0]))
		return date.year, date.month, date.day

	def calculate_bail_and_cost(some_units, requested_units, start, stop):
		days = (stop - start).days

		if days < 1:
			raise ValueError("deal must be at least 1 day long")

		ans_bail = 0
		ans_cost = 0
		for su in some_units:
			if days < su.rent_min_days:
				raise ValueError(f"unit with id={su['id']} has minimum rent duration of {su.rent_min_days}")

			requested = next((x for x in requested_units if x['id'] == su.id), None)
			if requested['count'] > su.count:
				raise ValueError(f"there is not enough units with id: {su.id}")
			ans_bail += su.bail
			ans_cost += su.first_day_cost + (days - 1)*su.day_cost
			# su.count -= requested['count']
			# su.save()

		return ans_bail, ans_cost

	try:
		start_year, start_month, start_day = get_date(request.POST['start-date'])
		stop_year, stop_month, stop_day = get_date(request.POST['stop-date'])
		start_date = datetime(start_year, start_month, start_day)
		stop_date = datetime(stop_year, stop_month, stop_day)
	except ValueError:
		return HttpResponse("wrong format of start/stop date. Must be DD.MM.YYYY", status=500)

	units_ids = [int(x['id']) for x in units]
	base_units = Unit.objects.filter(
		id__in=units_ids, is_deleted=False, published=True, owner__id=request.POST['owner'])
	if len(base_units) != len(units_ids):
		return HttpResponse("some units are not accessible", status=500)  # здесь есть защита от плохого owner и товаров

	try:
		bail, cost = calculate_bail_and_cost(base_units, units, start_date, stop_date)

		# FIXME: вклюить эту проверку, когда фронт будет готов
		"""
		if bail != int(request.POST['bail']):  
			raise ValueError("bail mismatch")
		if cost != int(request.POST['cost']):
			raise ValueError('cost mismatch')
		"""
	except ValueError as e:
		return HttpResponse("error in bail/cost calculation: " + str(e), status=500)

	order = Order.objects.create(
		owner=User.objects.get(id=request.POST['owner']),
		client=request.user,
		status="init",
		commentary=request.POST['commentary'],
		start_date=start_date,
		stop_date=stop_date,
		bail=bail,
		cost=cost,
	)
	order_units = [OrderUnit(
		order=order,
		unit=bu) for bu in base_units]

	OrderUnit.objects.bulk_create(order_units)

	return HttpResponse("OK")
