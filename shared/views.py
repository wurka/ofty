from django.shortcuts import HttpResponse
from django.middleware.csrf import get_token


# Create your views here.
def get_csrf_token(request):
	token = get_token(request)
	return HttpResponse(token)


def get_full_url(request):
	full_url = request.build_absolute_uri("/")
	return HttpResponse(full_url)
