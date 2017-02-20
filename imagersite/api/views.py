from imager_images.models import Photos, Albums
from api.serializers import PhotoSerializer
from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions


class PhotoViewSet(viewsets.ModelViewSet, LoginRequiredMixin):

    serializer_class = PhotoSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        """Get queryset for logged in photographer."""
        return Photos.objects.filter(photographer__id=self.request.user.id)
