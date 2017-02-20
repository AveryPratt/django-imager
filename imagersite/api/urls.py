from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import PhotoViewSet


urlpatterns = [
    url(r'^photos/$', PhotoViewSet.as_view({'get': 'list'}), name='api_photos'),
]

urlpatterns = format_suffix_patterns(urlpatterns)