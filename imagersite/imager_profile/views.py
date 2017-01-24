from django.shortcuts import render
from django.http import HttpResponse
from imager_images.models import Photos, Albums
from django.core.urlresolvers import reverse_lazy
from django.conf import settings


def home_view(request):
    """Home view callable, for the home page."""
    import random
    photos = Photos.objects.all()
    if len(photos) > 0:
        photo_url = random.choice(photos).image.url
    else:
        photo_url = settings.media_url + "Capture3.PNG"
    return render(request, "imagersite/home.html", {"photo_url": photo_url})


# def login_view(request):
#     return render(request, "imagersite/registration/login.html")


# def logout_view(request):
#     return HttpResponse()
