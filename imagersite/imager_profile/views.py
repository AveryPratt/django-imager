from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

import random

from imager_images.models import Photos, Albums
from imager_profile.models import ImagerProfile


class HomeView(TemplateView):
    """Class-based view for home page."""

    template_name = "imagersite/home.html"

    def get_context_data(self):
        photos = Photos.objects.all()
        if len(photos) > 0:
            photo = random.choice(photos)
            photo_url = random.choice(photos).image.url
        else:
            photo = None
            photo_url = settings.media_url + "standard.jpg"
        return {"photo": photo, "photo_url": photo_url}


class UserProfileView(TemplateView):
    """Class based view for user's personal profile."""

    template_name = "imager_profile/profile.html"

    def get_context_data(self):
        user = self.request.user
        if user.is_authenticated():
            photos = Photos.objects.all().filter(
                photographer_id=user.profile.id)
            public_photos = photos.filter(published='PU').count()
            private_photos = photos.filter(published="PR").count()
            shared_photos = photos.filter(published="SH").count()
            albums = Albums.objects.all().filter(id=user.profile.id)
            return {
                    "user": user,
                    "private_photos": private_photos,
                    "public_photos": public_photos,
                    "shared_photos": shared_photos,
                    "albums": albums}


class ProfileView(TemplateView):
    """Class based view for everyone's public profile."""

    template_name = "imager_profile/profile.html"

    def get_context_data(self, username):
        user = get_object_or_404(User, username=username.capitalize())
        photos = Photos.objects.all().filter(id=user.id)
        public_photos = photos.filter(published='PU').count()
        albums = Albums.objects.all().filter(id=user.id)
        return {
                "user": user.username,
                "photos": photos,
                "public_photos": public_photos,
                "albums": albums}
