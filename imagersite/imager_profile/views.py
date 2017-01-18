from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader


def home_view(request):
    """Home view callable, for the home page."""
    # template = loader.get_template("imagersite/home.html")
    # response = template.render({"beg_for_it": "Please"})
    return render(request, "imagersite/home.html", {"beg_for_it": "Please"})


def login_view(request):
    # template = loader.get_template("imagersite/login.html")
    return render(request, "imagersite/login.html")


def logout_view(request):
    return HttpResponse("logout")
