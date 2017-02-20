from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from imager_images.models import Photos, Albums
from imager_images.forms import AddAlbumForm, AddPhotoForm, EditAlbumForm, EditPhotoForm

# Create your views here.


class LibraryView(ListView, LoginRequiredMixin):
    """Class-based view for user's library."""

    template_name = "imager_images/library.html"
    model = Photos
    paginate_by = 4

    def get_context_data(self):
        """Get context data so you can work with multiple models."""
        albums = Albums.objects.filter(
            photographer_id=self.request.user.profile.id)
        photos = Photos.objects.filter(
            photographer_id=self.request.user.profile.id)

        page = self.request.GET.get("page")
        photo_paginator = Paginator(photos, self.paginate_by)
        album_paginator = Paginator(albums, self.paginate_by)

        try:
            photo_pages = photo_paginator.page(page)
            album_pages = album_paginator.page(page)
        except PageNotAnInteger:
            photo_pages = photo_paginator.page(1)
            album_pages = album_paginator.page(1)
        except EmptyPage:
            photo_pages = photo_paginator.page(photo_paginator.num_pages)
            album_pages = album_paginator.page(album_paginator.num_pages)

        return {"photos": photo_pages, "albums": album_pages}


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
        tags = photo.tag.all()
        similar_photos = Photos.objects.filter(tag__in=tags).exclude(
            id=photo.id).distinct()
        return {"photo": photo, "similar_photos": similar_photos[:5]}


class AddPhotoView(LoginRequiredMixin, CreateView):
    """Class-based view for creating photos."""

    model = Photos
    form_class = AddPhotoForm
    template_name = 'imager_images/add_photo.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        photo = form.save()
        photo.photographer = self.request.user.profile
        photo.published_date = timezone.now()
        photo.save()
        return redirect('library')


class EditPhotoView(LoginRequiredMixin, UpdateView):
    """Class-based view for editing photos."""

    model = Photos
    form_class = EditPhotoForm
    template_name = 'imager_images/edit_photo.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('library')


class RemovePhotoView(LoginRequiredMixin, DeleteView):
    """Delete a photo."""

    template_name = "imager_images/remove_photo.html"
    model = Photos
    login_url = reverse_lazy("login")

    def delete(self, request, pk=None):
        self.photo = Photos.objects.get(pk=pk)
        self.photo.delete()
        return redirect('photo_gallery')


class AlbumGalleryView(ListView):
    """Class-based view for user's album gallery."""

    template_name = "imager_images/album_gallery.html"
    model = Albums
    context_object_name = 'albums'
    paginate_by = 4
    queryset = Albums.objects.all().filter(published='PU')


class AlbumDetailView(TemplateView):
    """Class-based view for individual albums."""

    template_name = "imager_images/album_detail.html"
    model = Albums
    paginate_by = 4

    def get_context_data(self, id):
        """Get context data so you can work with two models."""
        album = Albums.objects.filter(id=id).first()
        photos = Photos.objects.filter(album__id=id)

        paginator = Paginator(photos, self.paginate_by)
        page = self.request.GET.get("page")

        try:
            photo_pages = paginator.page(page)
        except PageNotAnInteger:
            photo_pages = paginator.page(1)
        except EmptyPage:
            photo_pages = paginator.page(paginator.num_pages)

        return {"album": album, "photos": photo_pages}


class AddAlbumView(LoginRequiredMixin, CreateView):
    """Class-based view for creating albums."""

    model = Albums
    form_class = AddAlbumForm
    template_name = 'imager_images/add_album.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        album = form.save()
        album.photographer = self.request.user.profile
        album.published_date = timezone.now()
        album.save()
        return redirect('library')


class RemoveAlbumView(LoginRequiredMixin, DeleteView):
    """Delete a photo."""

    template_name = "imager_images/remove_album.html"
    model = Albums
    login_url = reverse_lazy("login")

    def delete(self, request, pk=None):
        self.album = Albums.objects.get(pk=pk)
        self.album.delete()
        return redirect('album_gallery')


class EditAlbumView(LoginRequiredMixin, UpdateView):
    """Class-based view for editing albums."""

    model = Albums
    form_class = EditAlbumForm
    template_name = 'imager_images/edit_album.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('library')
