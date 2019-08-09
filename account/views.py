from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from account.models import OftyUser


# Create your views here.
def login(request):
	# TODO: сделать тут POST запросы, когда будет интерфеечка
	if "user" not in request.POST:
		return HttpResponse("specify user, please", status=500)
	if "password" not in request.POST:
		return HttpResponse("specify password, please", status=500)

	user = authenticate(username=request.POST["user"], password=request.POST["password"])
	if user is not None:
		django_login(request, user)
		return HttpResponse("OK")
	else:
		return HttpResponse("login failed", status=500)


def logout(request):
	request.user.logout()
	if request.user.is_anonymous:
		return HttpResponse("OK")
	else:
		return HttpResponse("something going wrong with logout", status=500)


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


def time_set(request):
	return HttpResponse("time set not implemented")


def new_account(request):
	must = ["login", "password"]
	for m in must:
		if m not in request.POST:
			return HttpResponse(f"There is no parameter {m}", status=500)
	try:
		User.objects.get(username=request.POST['login'])
		return HttpResponse("login already exists", status=500)
	except User.DoesNotExist:
		new_user = User.objects.create_user(
			username=request.POST["login"],
			email="",
			password=request.POST['password'])
		OftyUser.objects.create(user=new_user)
		return HttpResponse("OK")
