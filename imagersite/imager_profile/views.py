from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView

import random

from imager_images.models import Photos, Albums
from imager_profile.models import ImagerProfile
from imager_profile.forms import EditProfileForm, EditUserForm


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
            photo_url = settings.MEDIA_URL + "standard.jpg"
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
    user_form_class = EditUserForm
    template_name = 'imager_profile/edit_profile.html'
    login_url = reverse_lazy('login')
    permission_required = "imager_profile.edit_profile"
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        # import pdb; pdb.set_trace()
        return self.request.user.profile.user

    def form_valid(self, profile_form, user_form):
        """If the form is successful, update user profile."""
        self.object = profile_form.save()
        import pdb; pdb.set_trace()
        self.object.user.profile.user.first_name = user_form.cleaned_data['first_name']
        self.object.user.profile.user.last_name = user_form.cleaned_data['last_name']
        self.object.user.profile.user.email = user_form.cleaned_data['email']
        self.object.user.profile.camera = profile_form.cleaned_data['camera']
        self.object.user.profile.address = profile_form.cleaned_data['address']
        self.object.user.profile.bio = profile_form.cleaned_data['bio']
        self.object.user.profile.website = profile_form.cleaned_data['website']
        self.object.user.profile.hireable = profile_form.cleaned_data['hireable']
        self.object.user.profile.travel_radius = profile_form.cleaned_data['travel_radius']
        self.object.user.profile.phone = profile_form.cleaned_data['phone']
        self.object.user.photography_type = profile_form.cleaned_data['photography_type']
        self.object.user.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProfileView(TemplateView):
    """Class based view for everyone's public profile."""

    template_name = "imager_profile/profile.html"

    def get_context_data(self, username):
        user = get_object_or_404(User, username=username.capitalize())
        photos = Photos.objects.all().filter(id=user.id)
        public_photos = photos.filter(published='PU').count()
        albums = Albums.objects.all().filter(id=user.id)
        return {
                "user": user,
                "photos": photos,
                "public_photos": public_photos,
                "albums": albums}
