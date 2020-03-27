from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from units.views import units_to_json
from .models import Basket, BasketUnit
from units.views import logged, get_with_parameters, post_with_parameters
from units.models import Unit
from account.models import OftyUser
from ofty.consumers import UserUpdateConsumer


@logged
@get_with_parameters()
def get_content(request):
	basket_units = [b.unit for b in BasketUnit.objects.filter(basket__user=request.user).order_by('unit__owner')]
	json_units = units_to_json(request, basket_units)

	blocks = list()
	last_owner = None
	for i, unit in enumerate(basket_units):
		if unit.owner != last_owner:
			# создаём новый блок
			o_user = OftyUser.get_user(unit.owner)
			blocks.append({
				'owner': {
					'id': unit.owner.id,
					'name': o_user.nickname,
					'rent-commentary': o_user.rent_commentary
				},
				'units': []
			})

			last_owner = unit.owner
		if unit.is_deleted:
			blocks[-1]['units'].append({
				'type': 'deleted-unit',
				'data': ''
			})
		elif not unit.published:
			blocks[-1]['units'].append({
				'type': 'unpublished-unit',
				'data': ''
			})
		else:
			blocks[-1]['units'].append({
				'type': 'unit',
				'data': json_units[i]
			})

	return JsonResponse(blocks, safe=False)


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
		BasketUnit.objects.get(basket__user=request.user, unit=unit)
		return HttpResponse("unit already in basket", status=500)
	except BasketUnit.DoesNotExist:
		basket = Basket.get_basket(request.user)
		new_basket_unit = BasketUnit.objects.create(basket=basket, unit=unit)

		my_units = BasketUnit.objects.filter(basket=basket)
		ofty_user = OftyUser.get_user(request.user)
		ofty_user.units_in_basket = len(my_units)

		UserUpdateConsumer.notifty_user(request.user)
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

		my_units = BasketUnit.objects.filter(basket=basket)
		ofty_user = OftyUser.get_user(request.user)
		ofty_user.units_in_basket = len(my_units)
	except BasketUnit.DoesNotExist:
		return HttpResponse('unit not in basket', status=500)

	return HttpResponse("OK")
