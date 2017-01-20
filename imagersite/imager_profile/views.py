from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    """Home view callable, for the home page."""
    return render(request, "imagersite/home.html", {"foo": "bar"})


def login_view(request):
    return render(request, "imagersite/registration/login.html")


# def logout_view(request):
#     return HttpResponse()
