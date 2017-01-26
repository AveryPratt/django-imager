from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone

from imager_images.models import Photos, Albums
from imager_images.forms import AddAlbumForm, AddPhotoForm

# Create your views here.


class LibraryView(TemplateView):
    """Class-based view for library page."""

    template_name = "imager_images/library.html"

    def get_context_data(self):
        """Library view callable, for a user's library page."""
        if self.request.user.is_authenticated():
            user = self.request.user
            photos = Photos.objects.all().filter(photographer_id=user.profile.id)
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
        photos = Photos.objects.filter(album__id=id)
        return {"photos": photos}


class AddPhotoView(CreateView):
    """Class-based view for creating photos."""

    login_required = True
    model = Photos
    form_class = AddPhotoForm
    template_name = 'imager_images/add_photo.html'
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        photo = form.save()
        photo.photographer = self.request.user.profile
        photo.published_date = timezone.now()
        photo.save()
        return redirect('photo_detail', id=photo.id)


class AddAlbumView(CreateView):
    """Class-based view for creating albums."""

    template_name = "imager_images/add_album.html"

    def get_context_data(self):
        """Add Album view callable, for adding albums."""
        form = AddAlbumForm
        return {"form": form}
