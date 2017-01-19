from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth import 
# from django.template import loader


def home_view(request):
    """Home view callable, for the home page."""
    # template = loader.get_template("imagersite/home.html")
    # response = template.render({"beg_for_it": "Please"})
    return render(request, "imagersite/home.html")


def login_view(request):
    # template = loader.get_template("imagersite/login.html")
    return render(request, "imagersite/registration/login.html")


# def logout_view(request):
#     return HttpResponse()
