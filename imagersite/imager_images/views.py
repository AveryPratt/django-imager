from django.shortcuts import render
from imager_images.models import Photos, Albums

# Create your views here.


def library_view(request):
    """Library view callable, for a user's library page."""
    if request.user.is_authenticated():
        user = request.user
        photos = Photos.objects.all().filter(photographer_id=user.profile.id)
        albums = Albums.objects.all().filter(id=user.profile.id)
        return render(
            request, "imager_images/library.html", {
                                        "user": user,
                                        "photos": photos,
                                        "albums": albums})


def photo_gallery_view(request):
    """Display all public photos by all users."""
    photos = Photos.objects.all().filter(published='PU')
    return render(
        request, "imager_images/photo_gallery.html", {"photos": photos})


def photo_detail_view(request, id):
    """Displays a single photo when clicked on by user."""
    photo = Photos.objects.get(id=id)
    return render(request, "imager_images/photo_detail.html", {"photo": photo})


def album_gallery_view(request):
    """Display all public albums by all users."""
    albums = Albums.objects.all().filter(published='PU')
    return render(
        request, "imager_images/album_gallery.html", {"albums": albums})


def album_detail_view(request, id):
    """Displays a single album when clicked on by user."""
    photos = Photos.objects.filter(album__id=id)
    return render(
        request, "imager_images/album_detail.html", {"photos": photos})
