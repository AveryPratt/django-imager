"""Tests for the imager_profile on imagersite."""


from django.test import TestCase
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory

# Create your tests here.


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    class UserFactory(factory.django.DjangoModelFactory):
        """Factory for building new user objects."""

        class Meta:
            """Set up which model this factory will build from."""

            model = User

        username = factory.Sequence(lambda n: "The Chosen {}".format(n))
        email = factory.LazyAttribute(
            lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
        )

    def setUp(self):
        """The appropriate setup for the appropriate test."""
        self.users = [self.UserFactory.create() for i in range(20)]

    # def test_profile_is_made_when_user_is_saved(self):
    #     """When a user is saved, profiles are saved."""
    #     self.assertTrue(ImagerProfile.objects.count() == 20)

    # def test_profile_is_associated_with_actual_users(self):
    #     """When users are saved, profiles are associated with them."""
    #     profile = ImagerProfile.objects.first()
    #     self.assertTrue(hasattr(profile, "user"))
    #     self.assertIsInstance(profile.user, User)

    # def test_user_has_profile_attached(self):
    #     """Same as above, but from the user side."""
    #     user = self.users[0]
    #     self.assertTrue(hasattr(user, "profile"))
    #     self.assertIsInstance(user.profile, ImagerProfile)
