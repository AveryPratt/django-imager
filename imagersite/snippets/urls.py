from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^snippets/$', views.ImageList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.ImageDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
