from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView

import random

from imager_images.models import Photos, Albums
from imager_profile.models import ImagerProfile
from imager_profile.forms import EditProfileForm


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


class UserProfileView(
        LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Class based view for user's personal profile."""

    template_name = "imager_profile/user_profile.html"
    login_url = reverse_lazy("login")
    permission_required = "imager_profile.see_profile"

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


class EditProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit your user profile."""
    model = ImagerProfile
    form_class = EditProfileForm
    template_name = 'imager_profile/edit_profile.html'
    login_url = reverse_lazy('login')
    permission_required = "imager_profile.edit_profile"
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        # import pdb;pdb.set_trace()
        return self.request.user.profile


class ProfileView(TemplateView):
    """Class based view for everyone's public profile."""

    template_name = "imager_profile/profile.html"

    def get_context_data(self, username):
        # import pdb;pdb.set_trace()
        user = get_object_or_404(User, username=username.capitalize())
        photos = Photos.objects.all().filter(id=user.id)
        public_photos = photos.filter(published='PU').count()
        albums = Albums.objects.all().filter(id=user.id)
        return {
                "user": user,
                "photos": photos,
                "public_photos": public_photos,
                "albums": albums}
