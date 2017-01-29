"""Django form objects for profile model"""
from django import forms
from imager_profile.models import ImagerProfile


class EditProfileForm(forms.ModelForm):
    """Form for uploading a photo."""
    class Meta:
        """Meta stuff."""
        model = ImagerProfile
        exclude = []
