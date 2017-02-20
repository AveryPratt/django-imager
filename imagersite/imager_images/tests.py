from django.test import TestCase, Client, RequestFactory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    EditAlbumView,
    TagListView
)
import factory
from django.urls import reverse_lazy


# Create your tests here.


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "Imgr User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@site.com".format(x.username.replace(" ", "")))


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
        self.assertTrue(Albums.objects.first().date_uploaded)

    def test_album_date_modified(self):
        """Test that album has a date_modified."""
        self.assertTrue(Albums.objects.first().date_modified)

    def test_album_date_published(self):
        """Test that album has a date_published."""
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
        self.assertFalse(album.photographer)

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

    def test_photo_gallery_view(self):
        """Test that photo gallery view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        view = PhotoGalleryView.as_view()
        req = self.request.get("/photos/")
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_tag_list_view(self):
        """Test that photo gallery view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        view = TagListView.as_view()
        req = self.request.get("/tagged/")
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_photo_detail_view(self):
        """Test that photo detail view returns 200 OK response."""
        photo = ImageFactory()
        photo.save()
        view = PhotoDetailView.as_view()
        response = self.client.get(reverse_lazy("photo_detail", kwargs={"id": photo.id}))
        self.assertTrue(response.status_code == 200)

    def test_add_photo_view(self):
        """Test that add photo view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        view = AddPhotoView.as_view()
        req = self.request.get(reverse_lazy("add_photo"))
        req.user = user
        response = view(req)
        print(response.status_code)
        self.assertTrue(response.status_code == 200)

    def test_edit_photo_view(self):
        """Test that edit photo view returns 200 OK response."""
        user1 = User()
        user1.save()
        photo = ImageFactory()
        photo.save()
        self.client.force_login(user1)
        response = self.client.get(reverse_lazy("photo_edit", kwargs={"pk": photo.id}))
        self.assertTrue(response.status_code == 200)

    def test_remove_photo_view(self):
        """Test that remove photo view returns 200 OK response."""
        user1 = User()
        user1.save()
        photo = ImageFactory()
        photo.save()
        self.client.force_login(user1)
        response = self.client.get(reverse_lazy("remove_photo", kwargs={"pk": photo.id}))
        self.assertTrue(response.status_code == 200)

    def test_album_gallery_view(self):
        """Test that album gallery view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        view = AlbumGalleryView.as_view()
        req = self.request.get("/albums/")
        req.user = user
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_album_detail_view(self):
        """Test that album detail view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        album = AlbumFactory()
        album.save()
        view = AlbumDetailView.as_view()
        response = self.client.get(reverse_lazy("album_detail", kwargs={"id": album.id}))
        self.assertTrue(response.status_code == 200)

    def test_add_album_view(self):
        """Test that add album view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        view = AddAlbumView.as_view()
        req = self.request.get(reverse_lazy("add_album"))
        req.user = user
        response = view(req)
        print(response.status_code)
        self.assertTrue(response.status_code == 200)

    def test_remove_album_view(self):
        """Test that remove album view returns 200 OK response."""
        user = UserFactory.create()
        user.save()
        album = AlbumFactory()
        album.save()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("remove_album", kwargs={"pk": album.id}))
        self.assertTrue(response.status_code == 200)

    def test_edit_album_view(self):
        """Test that edit album view returns 200 OK response."""
        user1 = User()
        user1.save()
        album = AlbumFactory()
        album.save()
        self.client.force_login(user1)
        response = self.client.get(reverse_lazy("album_edit", kwargs={"pk": album.id}))
        self.assertTrue(response.status_code == 200)


class PaginationTests(TestCase):
    """Test pagination."""

    def setUp(self):
        """User setup for tests."""
        self.client = Client()
        self.request = RequestFactory()
        self.users = UserFactory.create()
        self.images = [ImageFactory.create() for i in range(10)]
        self.albums = [AlbumFactory.create() for i in range(10)]

    def test_photo_paginator(self):
        """Test that 10 photos in groups of 4 create 3 pages."""
        paginator = Paginator(self.images, 4)
        self.assertEqual(10, paginator.count)
        self.assertEqual(3, paginator.num_pages)
        self.assertEqual([1, 2, 3], list(paginator.page_range))

    def test_album_paginator(self):
        """Test that 10 albums in groups of 4 create 3 pages."""
        paginator = Paginator(self.albums, 4)
        self.assertEqual(10, paginator.count)
        self.assertEqual(3, paginator.num_pages)
        self.assertEqual([1, 2, 3], list(paginator.page_range))

    def test_empty_page_photos(self):
        """Test that a nonexistent page raises the EmptyPage exception."""
        paginator = Paginator(self.images, 4)
        self.assertRaises(EmptyPage, paginator.page, 15)

    def test_empty_page_albums(self):
        """Test that a nonexistent page raises the EmptyPage exception."""
        paginator = Paginator(self.images, 4)
        self.assertRaises(EmptyPage, paginator.page, 15)

    def test_invalid_page(self):
        """Test that PageNotAnInteger gets raised when you pass in a string."""
        paginator = Paginator(self.albums, 4)
        self.assertRaises(PageNotAnInteger, paginator.page, 'a')