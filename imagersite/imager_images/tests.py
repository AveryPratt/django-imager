from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_images.models import Photos, Albums
from imager_profile.models import ImagerProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from imager_images.views import (
    LibraryView,
    PhotoGalleryView,
    PhotoDetailView,
    AddPhotoView,
    EditPhotoView,
    RemovePhotoView,
    AlbumGalleryView,
    AlbumDetailView,
    AddAlbumView,
    RemoveAlbumView,
    EditAlbumView
)
import factory


# Create your tests here.


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "Imgr User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@site.com".format(x.username.replace(" ", ""))
)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photos
    title = factory.Sequence(lambda n: "Image {}".format(n))
    image = SimpleUploadedFile(name='index.jpeg', content=open('imager_profile/static/images/dog.jpg', 'rb').read(), content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Albums
    title = factory.Sequence(lambda n: "Album {}".format(n))
    cover = SimpleUploadedFile(name='index.jpeg', content=open('imager_profile/static/images/dog.jpg', 'rb').read(), content_type='image/jpeg')
    description = "Dog!"


class ImageTestCase(TestCase):

    def setUp(self):
        """User setup for tests."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = [UserFactory.create() for i in range(10)]
        self.images = [ImageFactory.create() for i in range(10)]
        self.album = [AlbumFactory.create() for i in range(10)]

    def test_image_title(self):
        """Test that image has "Image" in title."""
        image = Photos.objects.first()
        self.assertTrue("Image" in image.title)

    def test_image_description(self):
        """Test that the Image description field can be assigned."""
        image = Photos.objects.first()
        image.description = "This is a good image."
        image.save()
        self.assertTrue(Photos.objects.first().description == "This is a good image.")

    def test_image_date_modified(self):
        """Test that the image has a date modified default."""
        image = Photos.objects.first()
        self.assertTrue(image.date_modified)

    def test_image_date_uploaded(self):
        """Test that the image has a date uploaded default."""
        image = Photos.objects.first()
        self.assertTrue(image.date_uploaded)

    def test_image_date_published(self):
        """Test that the image has a date published."""
        image = Photos.objects.first()
        self.assertTrue(image.date_published)

    def test_image_published(self):
        """Test the image published field."""
        image = Photos.objects.first()
        image.published = "public"
        image.save()
        self.assertTrue(Photos.objects.first().published == "public")

    def test_image_no_photographer(self):
        """Test that image has no photographer."""
        image = Photos.objects.first()
        self.assertFalse(image.photographer)

    def test_image_photographer(self):
        """Test that image can be assigned a photographer"""
        image = Photos.objects.first()
        photographer = ImagerProfile.objects.first()
        image.photographer = photographer
        image.save()
        self.assertTrue(Photos.objects.first().photographer == photographer)

    def test_image_no_album(self):
        """Test that image has no album."""
        image = Photos.objects.first()
        self.assertFalse(image.album)

    def test_image_album(self):
        """Test that image can be assigned an album."""
        image = Photos.objects.first()
        album = Albums.objects.first()
        image.album = album
        image.save()
        self.assertTrue(Photos.objects.first().album == album)

    def test_album_title(self):
        """Test that album has a title."""
        album = Albums.objects.first()
        self.assertTrue("Album" in album.title)

    def test_album_description(self):
        """Test that album can have a description."""
        album = Albums.objects.first()
        album.description = "description."
        album.save()
        self.assertTrue(Albums.objects.first().description == "description.")

    def test_album_date_uploaded(self):
        """Test that album has a date_uploaded."""
        album = Albums.objects.first()
        self.assertTrue(Albums.objects.first().date_uploaded)

    def test_album_date_modified(self):
        """Test that album has a date_modified."""
        album = Albums.objects.first()
        self.assertTrue(Albums.objects.first().date_modified)

    def test_album_date_published(self):
        """Test that album has a date_published."""
        album = Albums.objects.first()
        self.assertTrue(Albums.objects.first().date_published)

    def test_album_default_published(self):
        """Test that album is public by default."""
        album = Albums.objects.first()
        self.assertTrue(album.published == "PU")

    def test_album_published(self):
        """Test that album is public by default."""
        album = Albums.objects.first()
        album.published = "public"
        album.save()
        self.assertTrue(Albums.objects.first().published == "public")

    def test_album_default_cover(self):
        """Test that album has a default cover."""
        album = Albums.objects.first()
        self.assertTrue(album.cover)

    def test_album_cover(self):
        """Test that album has cover."""
        album = Albums.objects.first()
        cover = Photos.objects.first().image
        album.cover = cover
        album.save()
        self.assertTrue(Albums.objects.first().cover == cover)

    def test_album_no_photographer(self):
        """Test that album has no default photographer."""
        album = Albums.objects.first()
        self.assertFalse(Albums.objects.first().photographer)

    def test_album_photographer(self):
        """Test that album has a photographer."""
        album = Albums.objects.first()
        photographer = ImagerProfile.objects.first()
        album.photographer = photographer
        album.save()
        self.assertTrue(Albums.objects.first().photographer == photographer)

    def test_library_view(self):
        """Test that library view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        view = LibraryView.as_view()
        req = self.request.get("/library/")
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)