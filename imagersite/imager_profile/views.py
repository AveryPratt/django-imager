from django.shortcuts import render
from django.http import HttpResponse
from imager_images.models import Photos, Albums
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile


def home_view(request):
    """Home view callable, for the home page."""
    import random
    photos = Photos.objects.all()
    if len(photos) > 0:
        photo = random.choice(photos)
        photo_url = random.choice(photos).image.url
    else:
        photo = None
        photo_url = settings.media_url + "standard.jpg"
    return render(request, "imagersite/home.html", {"photo": photo, "photo_url": photo_url})


def user_profile_view(request):
    """Profile view callable for user's personal profile."""
    if request.user.is_authenticated():
        user = request.user
        photos = Photos.objects.all().filter(photographer_id=user.profile.id)
        public_photos = photos.filter(published='PU').count()
        private_photos = photos.filter(published="PR").count()
        shared_photos = photos.filter(published="SH").count()
        albums = Albums.objects.all().filter(id=user.profile.id)
        return render(
            request, "imager_profile/profile.html", {
                                        "user": user,
                                        "private_photos": private_photos,
                                        "public_photos": public_photos,
                                        "shared_photos": shared_photos,
                                        "albums": albums})


def profile_view(request, username):
    """Profile view callable for all profiles."""
    user = ImagerProfile.objects.get(user__username=username).user
    photos = Photos.objects.all().filter(id=user.id)
    public_photos = photos.filter(published='PU').count()
    albums = Albums.objects.all().filter(id=user.id)
    return render(
        request, "imager_profile/profile.html", {
                                            "user": user.username,
                                            "photos": photos,
                                            "public_photos": public_photos,
                                            "albums": albums})


# def login_view(request):
#     return render(request, "imagersite/registration/login.html")


# def logout_view(request):
#     return HttpResponse()
