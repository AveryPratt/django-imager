from django.shortcuts import render
from django.http import HttpResponse
from imager_images.models import Photos, Albums


def home_view(request):
    """Home view callable, for the home page."""
    photos = Photos.objects.all()
    albums = Albums.objects.all
    return render(request, "imagersite/home.html", {"photos": "photos", "albums": "albums"})


# def login_view(request):
#     return render(request, "imagersite/registration/login.html")


# def logout_view(request):
#     return HttpResponse()
