from django.contrib.auth.models import User
from rest_framework import serializers
from imager_images.models import Photos, Albums


class PhotoSerializer(serializers.ModelSerializer):
    photographer = serializers.ReadOnlyField(
        source='photographer.user.username')

    class Meta:
        model = Photos
        fields = ('title', 'description', 'date_uploaded',
                  'date_modified', 'date_published', 'published', 'image',
                  'photographer', 'album')
