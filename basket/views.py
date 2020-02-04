from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from units.views import units_to_json
from .models import Basket, BasketUnit
from units.views import logged, get_with_parameters, post_with_parameters
from units.models import Unit
from account.models import OftyUser


@logged
@get_with_parameters()
def get_content(request):
	basket_units = [b.unit for b in BasketUnit.objects.filter(user=request.user).order_by('unit__owner')]
	json_units = units_to_json(basket_units)

	units = list()
	last_owner = None
	for i, unit in enumerate(basket_units):
		if unit.owner != last_owner:
			units.append({
				'type': 'owner',
				'data': {
					'id': unit.owner.id,
					'name': OftyUser.get_user(unit.owner).nickname
				}
			})
			last_owner = unit.owner
		if unit.is_deleted:
			units.append({
				'type': 'unit-deleted',
				'data': ''
			})
		elif not unit.published:
			units.append({
				'type': 'unit-unpublished',
				'data': ''
			})
		else:
			units.append({
				'type': 'unit',
				'data': json_units[i]
			})

	return JsonResponse(units, safe=False)


@logged
@post_with_parameters('unit-id')
def add_unit(request):
	try:
		unit = Unit.objects.get(id=int(request.POST['unit-id']), is_deleted=False, published=True)
	except ValueError:
		return HttpResponse("unit-id must be integer", status=500)
	except Unit.DoesNotExist:
		return HttpResponse(f"unit not found, id={request.POST['unit-id']}", status=500)

	try:
		BasketUnit.objects.get(user=request.user, unit=unit)
		return HttpResponse("unit already in basket", status=500)
	except BasketUnit.DoesNotExist:
		new_basket_unit = BasketUnit.objects.create(user=request.user, unit=unit)

	return JsonResponse({'id': new_basket_unit.id})


@logged
@post_with_parameters("unit-id")
def remove_unit(request):
	try:
		unit = Unit.objects.get(id=int(request.POST['unit-id']), is_deleted=False, published=True)
	except ValueError:
		return HttpResponse('unit-id must be integer', status=500)
	except Unit.DoesNotExist:
		return HttpResponse("unit not found", status=500)

	try:
		basket = Basket.get_basket(request.user)
		bu = BasketUnit.objects.get(basket=basket, unit=unit)
		bu.delete()
	except BasketUnit.DoesNotExist:
		return HttpResponse('unit not in basket', status=500)

	return HttpResponse("OK")
