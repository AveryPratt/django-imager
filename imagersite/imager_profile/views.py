from django.http import HttpResponse


def home_view(request):
    """Home view callable, for the home page."""
    return HttpResponse("Hello World!")