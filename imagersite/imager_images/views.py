from django.shortcuts import render
from imager_images.models import Photos, Albums
from django.views.generic import TemplateView
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


class AddPhotoView(TemplateView):
    """Class-based view for creating photos."""

    template_name = "imager_images/add_photo.html"

    def get_context_data(self):
        """Add Photo view callable, for adding photos."""
        form = AddPhotoForm
        return {"form": form}


class AddAlbumView(TemplateView):
    """Class-based view for creating albums."""

    template_name = "imager_images/add_album.html"

    def get_context_data(self):
        """Add Album view callable, for adding albums."""
        form = AddAlbumForm
        return {"form": form}
