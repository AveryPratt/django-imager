from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_images.models import Photos, Albums
from imager_profile.models import ImagerProfile
from django.core.files.uploadedfile import SimpleUploadedFile
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
    image = SimpleUploadedFile(name='index.jpeg', content=open('imagersite/static/images/index.jpeg', 'rb').read(), content_type='image/jpeg')


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Albums
    title = factory.Sequence(lambda n: "Album {}".format(n))
    cover = SimpleUploadedFile(name='index.jpeg', content=open('imagersite/static/images/index.jpeg', 'rb').read(), content_type='image/jpeg')
    description = "Panda!"


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
        self.assertTrue("Image" in Photos.objects.first().title)

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
        self.assertTrue(image.photographer == photographer)

    def test_image_no_album(self):
        """Test that image has no album."""
        image = Photos.objects.first()
        self.assertFalse(image.album)

    def test_image_no_album(self):
        """Test that image can be assigned an album."""
        image = Photos.objects.first()
        album = Albums.objects.first()
        image.album = album
        self.assertTrue(image.album == album)