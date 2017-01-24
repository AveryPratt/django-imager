from django.db import models
from imager_profile.models import ImagerProfile

# Create your models here.


class Albums(models.Model):
    """."""
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    date_modified = models.DateField(blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    PUBLISHED_CHOICES = [
        ('PR', 'private'),
        ('SH', 'shared'),
        ('PU', 'public'),
    ]
    published = models.CharField(max_length=255, choices=PUBLISHED_CHOICES, default='PU')
    cover = models.ImageField(upload_to="photos")
    photographer = models.ForeignKey(ImagerProfile, related_name="created_by", blank=True, null=True)


class Photos(models.Model):
    """."""
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    date_modified = models.DateField(blank=True, null=True)
    date_published = models.DateField(blank=True, null=True)
    PUBLISHED_CHOICES = [
        ('PR', 'private'),
        ('SH', 'shared'),
        ('PU', 'public'),
    ]
    published = models.CharField(max_length=255, choices=PUBLISHED_CHOICES, default='PU')
    image = models.ImageField(upload_to="photos")
    photographer = models.ForeignKey(ImagerProfile, related_name="photographed_by", blank=True, null=True)
    album = models.ForeignKey(Albums, related_name="in_album", blank=True, null=True)
