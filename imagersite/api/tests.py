from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from api.views import PhotoViewSet

from imager_images.models import Photos, Albums
from imager_profile.models import ImagerProfile

import factory
import random


class UserFactory(factory.django.DjangoModelFactory):
        """Make instances of user model for testing."""

        class Meta:
            model = User

        username = factory.Sequence(lambda n: "User{}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@site.com".format(x.username.replace(" ", ""))
        )


class PhotoFactory(factory.django.DjangoModelFactory):
        """Make instances of photo model for testing."""

        class Meta:
            model = Photos

        title = factory.Sequence(lambda n: "Image {}".format(n))
        image = SimpleUploadedFile(name='index.jpeg', content=open('imager_profile/static/images/dog.jpg', 'rb').read(), content_type='image/jpeg')


class APITests(TestCase):
    """The Profile Model test runner for db stuff."""

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(20)]
        self.photos = [PhotoFactory.create() for i in range(20)]

    def make_user(self):
        """Make test user and return his profile."""
        user = UserFactory.create()
        user.username = 'JeanLuc'
        user.set_password('supersecret')
        photo = PhotoFactory.create()
        photo.photographer = user.username
        user.save()
        photo.save()
        return user

# ValueError: Cannot assign "'JeanLuc'": "Photos.photographer" must be a "ImagerProfile" instance.
    # def test_api_route_status_OK(self):
    #     """Test that any user can go to the url and get a status 200."""
    #     jeanluc = self.make_user()
    #     self.client.force_login(jeanluc)
    #     response = self.client.get(reverse_lazy("api_photos"))
    #     self.assertEqual(response.status_code, 200)

    def test_non_user_cannot_view_photos_in_api(self):
        """Test non user cannnot access the api endpoint of photos."""
        request = self.request.get(reverse_lazy("api_photos"))
        view = PhotoViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 403)
        self.assertTrue("Authentication credentials were not provided." in response.rendered_content.decode())

    # def test_api_photo_route_is_status_ok(self):
    #     """Test that the api photo route produces a status ok."""
    #     jeanluc = self.make_user()
    #     self.client.force_login(jeanluc)
    #     response = self.client.get(reverse_lazy("api_photos"))
    #     # request.user = jeanluc
    #     # view = PhotoViewSet.as_view()
    #     # response = view(request)
    #     # import pdb;pdb.set_trace()
    #     self.assertTrue(response.status_code == 200)

    # def test_api_returns_json(self):
    #     """Test that the api photo route returns json."""
    #     jeanluc = self.make_user()
    #     self.client.force_login(jeanluc)
    #     response = self.client.get(reverse_lazy("api_photos"))
    #     self.assertTrue("photographer" in response.content.decode())

    # def test_user_can_view_photos_in_api(self):
    #     """Test the user can access the api endpoint of their photos."""
    #     jeanluc = self.make_user()
    #     photo = self.photos[0]
    #     photo.photographer.user.username = jeanluc.username
    #     photo.title = 'starship enterprise'
    #     photo.save()
    #     self.client.force_login(jeanluc)
    #     request = self.request.get(reverse_lazy("api_photos"))
    #     request.user = jeanluc
    #     view = PhotoViewSet.as_view({'get': 'list'})
    #     response = view(request)
    #     self.assertTrue('starship enterprise' in response.rendered_content.decode())
