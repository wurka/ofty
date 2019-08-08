from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate


# Create your views here.
def login(request):
	# TODO: сделать тут POST запросы, когда будет интерфеечка
	if "user" not in request.GET:
		return HttpResponse("specify user, please", status=500)
	if "password" not in request.GET:
		return HttpResponse("specify password, please", status=500)

	user = authenticate(username=request.GET["user"], password=request.GET["password"])

	if user is not None:
		return HttpResponse("login success")
	else:
		return HttpResponse("login failed", status=500)


def login_page(request):
	return HttpResponse("Where is my login_page dude?")


def login_info(request):
	if not request.user.is_authenticated:
		return HttpResponse("You not loggined in. Go for /account/login with your user, password pair")
	else:
		return HttpResponse(f"You loggined as {request.user.username} ({request.user.id})")


def demo(request):
	params = {
		'user_name': request.user.username if not request.user.is_anonymous else "Anonymous",
		"user_id": request.user.id if not request.user.is_anonymous else "X"
	}
	return render(request, 'account/demo.html', params)


def password_set(request):
	return HttpResponse("password set")


def delivery_set(request):
	return HttpResponse("delivery set")

