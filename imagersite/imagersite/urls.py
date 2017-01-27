"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from imager_profile.views import HomeView, UserProfileView, ProfileView
from imager_images.views import (
    LibraryView,
    PhotoGalleryView,
    AlbumGalleryView,
    PhotoDetailView,
    AlbumDetailView,
    PhotoEditView,
    AlbumEditView,
    AddAlbumView,
    AddPhotoView,
    RemoveAlbumView,
    RemovePhotoView,
)
# import imager_images.urls as photo_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^profile/$', UserProfileView.as_view(), name='profile'),
    url(r'^profile/(?P<username>\w+)/$', ProfileView.as_view(), name="profile"),
    url(r'^images/library/$', LibraryView.as_view(), name='library'),
    url(r'^images/photos/$', PhotoGalleryView.as_view(), name='photo_gallery'),
    url(r'^images/photos/(?P<id>\d+)/$', PhotoDetailView.as_view(), name='photo_detail'),
    url(r'^images/photos/(?P<id>\d+)/edit/$', PhotoEditView.as_view(), name='photo_edit'),
    url(r'^images/photos/add/$', AddPhotoView.as_view(), name="add_photo"),
    url(r"^remove/photos/(?P<pk>\d+)$", RemovePhotoView.as_view(), name="remove_photo"),
    url(r'^images/albums/$', AlbumGalleryView.as_view(), name='album_gallery'),
    url(r'^images/albums/(?P<id>\d+)/$', AlbumDetailView.as_view(), name='album_detail'),
    url(r'^images/albums/(?P<id>\d+)/edit/$', AlbumEditView.as_view(), name='album_edit'),
    url(r'^images/albums/add/$', AddAlbumView.as_view(), name="add_album"),
    url(r"^remove/albums/(?P<pk>\d+)$", RemoveAlbumView.as_view(), name="remove_album"),
    url(r'^registration/', include('registration.backends.hmac.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
