"""Django Form Objects."""


from django import forms
from imager_images.models import Photos, Albums


class AddPhotoForm(forms.ModelForm):
    """Form for uploading a photo."""
    class Meta:
        """Meta stuff."""
        model = Photos
        exclude = []


class AddAlbumForm(forms.ModelForm):
    """Form for uploading a photo."""
    class Meta:
        """Meta stuff."""
        model = Albums
        exclude = []
