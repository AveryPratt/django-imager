from django.urls import reverse_lazy
from imager_images.models import Photos, Albums
from api.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


class PhotoViewSet(viewsets.ModelViewSet):

    login_url = reverse_lazy('login')
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Get queryset for logged in photographer."""
        return Photos.objects.filter(photographer__id=self.request.user.id)
