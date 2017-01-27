from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from imager_images.models import Photos, Albums
from imager_images.forms import AddAlbumForm, AddPhotoForm, EditAlbumForm, EditPhotoForm

# Create your views here.


class LibraryView(LoginRequiredMixin, TemplateView):
    """Class-based view for library page."""

    template_name = "imager_images/library.html"
    login_url = reverse_lazy("login")

    def get_context_data(self):
        """Library view callable, for a user's library page."""
        user = self.request.user
        photos = Photos.objects.all().filter(
            photographer_id=user.profile.id)
        albums = Albums.objects.all().filter(id=user.profile.id)
        return {
            "user": user,
            "photos": photos,
            "albums": albums
        }


class PhotoGalleryView(TemplateView):
    """Class-based view for user's photo gallery."""

    template_name = "imager_images/photo_gallery.html"

    def get_context_data(self):
        """Photo Gallery view callable, for a user's photo gallery page."""
        photos = Photos.objects.all().filter(published='PU')
        return {"photos": photos}


class PhotoDetailView(TemplateView):
    """Class-based view for individual photos."""

    template_name = "imager_images/photo_detail.html"

    def get_context_data(self, id):
        """Photo Detail view callable, for an individual photo."""
        photo = Photos.objects.get(id=id)
        return {"photo": photo}


class AlbumGalleryView(TemplateView):
    """Class-based view for user's album gallery."""

    template_name = "imager_images/album_gallery.html"

    def get_context_data(self):
        """Album Gallery view callable, for a user's albums page"""
        albums = Albums.objects.all().filter(published='PU')
        return {"albums": albums}


class AlbumDetailView(TemplateView):
    """Class-based view for individual albums."""

    template_name = "imager_images/album_detail.html"

    def get_context_data(self, id):
        """Album Detail view callable, for an individual album."""
        album = Albums.objects.all().filter(id=id).first()
        photos = Photos.objects.filter(album__id=id)
        return {"album": album, "photos": photos}


class AddPhotoView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Class-based view for creating photos."""

    # login_required = True
    model = Photos
    form_class = AddPhotoForm
    template_name = 'imager_images/add_photo.html'
    success_url = reverse_lazy('library')
    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_photo"

    def form_valid(self, form):
        photo = form.save()
        photo.photographer = self.request.user.profile
        photo.published_date = timezone.now()
        photo.save()
        return redirect('photo_detail', id=photo.id)


class PhotoEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Class-based view for editing photos."""

    # login_required = True
    model = Photos
    form_class = EditPhotoForm
    template_name = 'imager_images/edit_photo.html'
    success_url = reverse_lazy('library')
    login_url = reverse_lazy('login')
    permission_required = "imager_images.edit_photo"

    def form_valid(self, form, pk=None):
        photo = form.save()
        photo.id = pk
        photo.save()
        return redirect('photo_detail', id=pk)


class AddAlbumView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Class-based view for creating albums."""

    # login_required = True
    model = Albums
    form_class = AddAlbumForm
    template_name = 'imager_images/add_album.html'
    success_url = reverse_lazy('library')
    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_album"

    def form_valid(self, form):
        album = form.save()
        album.photographer = self.request.user.profile
        album.published_date = timezone.now()
        album.save()
        return redirect('album_detail', id=album.id)


class AlbumEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Class-based view for editing albums."""

    # login_required = True
    model = Albums
    form_class = EditAlbumForm
    template_name = 'imager_images/edit_album.html'
    success_url = reverse_lazy('library')
    login_url = reverse_lazy('login')
    permission_required = "imager_images.edit_album"

    def form_valid(self, form, pk=None):
        album = form.save()
        album.id = pk
        album.save()
        return redirect('album_detail', id=pk)


class RemovePhotoView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a photo."""

    template_name = "imager_images/remove_photo.html"
    model = Photos
    login_url = reverse_lazy("login")
    permission_required = [
        "imager_images.add_photo, imager_images.remove_photo"]

    def delete(self, request, pk=None):
        self.photo = Photos.objects.get(pk=pk)
        self.photo.delete()
        return redirect('photo_gallery')


class RemoveAlbumView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a photo."""

    template_name = "imager_images/remove_album.html"
    model = Albums
    login_url = reverse_lazy("login")
    permission_required = [
        "imager_images.add_album, imager_images.remove_album"]

    def delete(self, request, pk=None):
        self.album = Albums.objects.get(pk=pk)
        self.album.delete()
        return redirect('album_gallery')
