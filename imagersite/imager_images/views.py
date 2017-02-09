from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from imager_images.models import Photos, Albums
from imager_images.forms import AddAlbumForm, AddPhotoForm, EditAlbumForm, EditPhotoForm

# Create your views here.


class LibraryView(LoginRequiredMixin, ListView):
    """Class-based view for library page."""

    template_name = "imager_images/library.html"
    login_url = reverse_lazy("login")
    model = Photos
    queryset = Photos.objects.all()
    context_object_name = 'photos'
    paginate_by = 4

    def get_context_data(self):
        user = self.request.user
        return {
            'user': user,
            'photos': Photos.objects.filter(photographer_id=user.profile.id),
            'albums': Albums.objects.filter(id=user.profile.id),
            }


class PhotoGalleryView(ListView):
    """Class-based view for user's photo gallery."""

    model = Photos
    template_name = "imager_images/photo_gallery.html"
    context_object_name = 'photos'
    paginate_by = 4
    queryset = Photos.objects.all().filter(published='PU')


class TagListView(ListView):
    """The listing for tagged books."""
    template_name = "imager_images/photo_gallery.html"
    model = Photos

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug")
        photos = Photos.objects.filter(tag__slug=slug).all()
        return {"photos": photos, "slug": slug}


class PhotoDetailView(TemplateView):
    """Class-based view for individual photos."""

    template_name = "imager_images/photo_detail.html"

    def get_context_data(self, id):
        """Photo Detail view callable, for an individual photo."""
        photo = Photos.objects.get(id=id)
        # import pdb;pdb.set_trace()
        tags = photo.tag.all()
        similar_photos = Photos.objects.filter(tag__in=tags).exclude(
            id=photo.id).distinct()
        return {"photo": photo, "similar_photos": similar_photos[:5]}


class AddPhotoView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Class-based view for creating photos."""

    model = Photos
    form_class = AddPhotoForm
    template_name = 'imager_images/add_photo.html'
    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_photo"

    def form_valid(self, form):
        photo = form.save()
        photo.photographer = self.request.user.profile
        photo.published_date = timezone.now()
        photo.save()
        return redirect('library')


class EditPhotoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Class-based view for editing photos."""

    model = Photos
    form_class = EditPhotoForm
    template_name = 'imager_images/edit_photo.html'
    login_url = reverse_lazy('login')
    permission_required = 'imager_images.edit_photo'
    success_url = reverse_lazy('library')


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


class AlbumGalleryView(ListView):
    """Class-based view for user's album gallery."""

    template_name = "imager_images/album_gallery.html"
    model = Albums
    queryset = albums = Albums.objects.all().filter(published='PU')

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


class AddAlbumView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Class-based view for creating albums."""

    # login_required = True
    model = Albums
    form_class = AddAlbumForm
    template_name = 'imager_images/add_album.html'
    login_url = reverse_lazy('login')
    permission_required = "imager_images.add_album"

    def form_valid(self, form):
        album = form.save()
        album.photographer = self.request.user.profile
        album.published_date = timezone.now()
        album.save()
        return redirect('library')


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


class EditAlbumView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Class-based view for editing albums."""

    model = Albums
    form_class = EditAlbumForm
    template_name = 'imager_images/edit_album.html'
    login_url = reverse_lazy('login')
    permission_required = "imager_images.edit_album.html"
    success_url = reverse_lazy('library')
