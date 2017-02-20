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
from imager_profile.views import HomeView, UserProfileView, ProfileView, EditProfileView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^profile/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^profile/edit/$', EditProfileView.as_view(), name="edit_profile"),
    url(r'^profile/(?P<username>\w+)/$', ProfileView.as_view(), name="profile"),
    url(r'^images/', include('imager_images.urls')),
    url(r'^registration/', include('registration.backends.hmac.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
