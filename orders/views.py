from django.http import HttpResponse, JsonResponse
from .models import Order, OrderUnit
from shared.methods import logged, get_with_parameters, post_with_parameters
from units.models import UnitPhoto


# Create your views here.
@logged
@get_with_parameters("page")
def get_my_orders(request):
    orders = Order.objects.filter(client=request.user).order_by("id")

    ans = [{
        "status": order.status,
        "statusText": Order.get_status_text(order.status),
        "start": f"{order.start_date.day:02}.{order.start_date.month:02}.{order.start_date.year}",
        "stop": f"{order.stop_date.day:02}.{order.stop_date.month:02}.{order.stop_date.year}",
        "commentary": order.commentary,
        "cost": order.cost,
        "bail": order.bail,
        "pictures": [
            photo.get_url()
            for photo in [
                UnitPhoto.objects.filter(unit=order_unit.unit) for order_unit in OrderUnit.objects.filter(order=order)]]
    } for order in orders]

    return JsonResponse(ans, safe=False)


@logged
@post_with_parameters("")
def new_order(request):
    return HttpResponse("OK")
