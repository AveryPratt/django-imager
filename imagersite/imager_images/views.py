from django.shortcuts import render
from imager_images.models import Photos, Albums

# Create your views here.

def library_view(request):
    """Library view callable, for a user's library page."""
    if request.user.is_authenticated():
        user = request.user
        photos = Photos.objects.all().filter(photographer_id=user.profile.id)
        albums = Albums.objects.all().filter(id=user.profile.id)
        # import pdb; pdb.set_trace()
        return render(
            request, "imager_images/library.html", {
                                        "user": user,
                                        "photos": photos,
                                        "albums": albums})
