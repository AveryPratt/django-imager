from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from imager_images.views import (
    LibraryView,
    PhotoGalleryView,
    AlbumGalleryView,
    PhotoDetailView,
    AlbumDetailView,
    EditPhotoView,
    EditAlbumView,
    AddAlbumView,
    AddPhotoView,
    RemoveAlbumView,
    RemovePhotoView,
)

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^photos/$', PhotoGalleryView.as_view(), name='photo_gallery'),
    url(r'^photos/(?P<id>\d+)/$', PhotoDetailView.as_view(), name='photo_detail'),
    url(r'^photos/(?P<pk>\d+)/edit/$', EditPhotoView.as_view(), name='photo_edit'),
    url(r'^photos/add/$', AddPhotoView.as_view(), name="add_photo"),
    url(r"^remove/photos/(?P<pk>\d+)$", RemovePhotoView.as_view(), name="remove_photo"),
    url(r'^albums/$', AlbumGalleryView.as_view(), name='album_gallery'),
    url(r'^albums/(?P<id>\d+)/$', AlbumDetailView.as_view(), name='album_detail'),
    url(r'^albums/(?P<pk>\d+)/edit/$', EditAlbumView.as_view(), name='album_edit'),
    url(r'^albums/add/$', AddAlbumView.as_view(), name="add_album"),
    url(r"^remove/albums/(?P<pk>\d+)$", RemoveAlbumView.as_view(), name="remove_album"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
