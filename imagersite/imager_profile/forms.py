"""Django form objects for profile model"""
from django import forms
from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    """Form for editing a profile."""
    class Meta:
        """Meta stuff."""
        model = ImagerProfile
        exclude = []

class EditUserForm(forms.ModelForm):
    """Form for editing a user's profile."""
    class Meta:
        """Meta stuff."""
        model = User
        exclude = []
