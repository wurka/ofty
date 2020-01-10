from django.http import HttpResponse


def post_with_parameters(*args):
	def decor(method):
		def response(request):
			if request.method != "POST":
				return HttpResponse(f"please use POST request, not {request.method}", status=500)
			for param in args:
				if param not in request.POST:
					return HttpResponse(f"there is no parameter {param}", status=500)
			return method(request)
		return response
	return decor


def get_with_parameters(*args):
	def decor(method):
		def response(request):
			if request.method != "GET":
				return HttpResponse(f"please use GET request, not {request.method}", status=500)
			for param in args:
				if param not in request.GET:
					return HttpResponse(f"there is no parameter {param}", status=500)
			return method(request)
		return response
	return decor


def logged(method):
	def inner(request):
		if request.user.is_anonymous:
			return HttpResponse("you must be loggined in", status=401)
		return method(request)
	return inner
