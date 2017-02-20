from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from api.views import PhotoViewSet

from imager_images.models import Photos
from imager_profile.tests import UserFactory
import factory
import random


# class ImageFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Photos
#     title = factory.Sequence(lambda n: "Image {}".format(n))
#     image = SimpleUploadedFile(name='index.jpeg', content=open('imager_profile/static/images/dog.jpg', 'rb').read(), content_type='image/jpeg')
#     photographer = UserFactory.create()


# class APITestCase(TestCase):

#     def setUp(self):
#         """Setting up tests for API models, views."""
#         self.user = UserFactory.create(username='Jean-Luc', email="JL@jean-luc.com")
#         self.client = Client()
#         self.request = RequestFactory()
#         import pdb;pdb.set_trace()
#         self.photos = [ImageFactory.create() for i in range(11, 20)]

