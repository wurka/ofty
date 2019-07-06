from django.shortcuts import HttpResponse
from django.middleware.csrf import get_token


# Create your views here.
def get_csrf_token(request):
	token = get_token(request)
	return HttpResponse(token)
