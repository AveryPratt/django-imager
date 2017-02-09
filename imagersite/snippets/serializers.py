from rest_framework import serializers
from imager_images.models import Photos
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = ('id', 'title', 'description', 'date_uploaded', 'date_modified', 'date_published', 'published', 'image', 'photographer', 'album')
