from imager_images.models import Photos, Albums
from api.serializers import PhotoSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions, views
from rest_framework.views import APIView

# from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response


class PhotoViewSet(viewsets.ModelViewSet):

    serializer_class = PhotoSerializer

    def get_queryset(self):
        """Get queryset for photographer."""
        return Photos.objects.all()

# class GetContactByNumber(APIView):
#     """Retrieve a contact by their phone number."""

#     def get_object(self, number):
#         """Get contact with given number."""
#         return Contact.objects.get(number=number)

#     def get(self, request, number=None, format=None):
#         """Return json response."""
#         contact = self.get_object('+' + str(number))
#         serializer = ContactSerializer(contact)
#         return Response(serializer.data)