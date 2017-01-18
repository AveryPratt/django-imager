from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class ActiveProfileManager(models.Manager):
    """Create Model Manager for Active Profiles"""
    def get_queryset(self):
        """Return active users."""
        qs = super(ActiveProfileManager, self).get_queryset()
        return qs.filter(user__is_active__exact=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """The imager user and all their attributes."""

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE
        )
    objects = models.Manager()
    active = ActiveProfileManager()

    camera_choices = [
        ('N', 'Nikon'),
        ('C', 'Canon'),
        ('K', 'Kodak')
    ]
    camera = models.CharField(choices=camera_choices, max_length=5, blank=True)
    address = models.CharField(max_length=255, blank=True)
    bio = models.CharField(default="", max_length=1000, blank=True)
    website = models.CharField(max_length=255, default="", blank=True)
    hireable = models.BooleanField(default=True)
    travel_radius = models.IntegerField(blank=True)
    phone = models.IntegerField(blank=True)
    photography_types = [
        ('LS', 'landscape'),
        ('PT', 'portrait'),
        ('NA', 'nature'),
        ('AS', 'astronomy'),
    ]
    photography_type = models.CharField(choices=photography_types, max_length=10, blank=True)
    # def active(self):
    #     """Queries objects in self and returns those that are active."""
    #     pass

    # @property
    # def is_active(self):
    #     return self.user.is_active

    # def __repr__(self):
    #     return "User: " + self.user + ""

# @receiver
