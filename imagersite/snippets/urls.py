from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.image_list),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.image_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
