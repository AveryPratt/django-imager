"""Tests for the imager_profile on imagersite."""

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from imager_profile.models import ImagerProfile
import factory
from faker import Faker
import random

# Create your tests here.


def fake_profile_attrs(profile):
    """."""
    fake = Faker()
    profile.cameraaddress = fake.address()
    profile.bio = fake.paragraph()
    profile.travel_radius = 20 * random.random()
    profile.phone = random.randint(1000000000, 9999999999)
    profile.photography_type = "LS"
    profile.save()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for building new user objects."""

    class Meta:
        """Set up which model this factory will build from."""
        model = User

    username = factory.Sequence(lambda n: "The Chosen {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    def setUp(self):
        """Populates list of test users."""
        self.users = [UserFactory.create() for i in range(20)]
        # for profile in ImagerProfile.objects.all():
        #     .fake_profile_attrs(profile)

    def test_profile_is_made_when_user_is_saved(self):
        """When a user is saved, profiles are saved."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_profile_is_associated_with_actual_users(self):
        """When users are saved, profiles are associated with them."""
        profile = ImagerProfile.objects.first()
        self.assertTrue(hasattr(profile, "user"))
        self.assertIsInstance(profile.user, User)

    def test_user_has_profile_attached(self):
        """Same as above, but from the user side."""
        user = self.users[0]
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, ImagerProfile)

    def test_inactive_users_have_inactive_profiles(self):
        """."""
        this_user = self.users[0]
        this_user.is_active = False
        this_user.save()
        self.assertTrue(ImagerProfile.active.count() == User.objects.all().count() - 1)

    def test_changes_on_profile_mean_changes_on_user_profile(self):
        """."""
        this_user = self.users[0]
        this_profile = ImagerProfile.objects.get(user=this_user)
        this_profile.photography_type = "PT"
        this_profile.save()
        self.assertTrue(this_profile.photography_type == "PT")


class ProfileFrontEndTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()

    def test_home_view_is_status_ok(self):
        """Test route to home view without client info or headers."""
        from imager_profile.views import HomeView
        req = self.request.get("/potato")
        view = HomeView.as_view()
        response = view(req)
        self.assertTrue(response.status_code == 200)

    def test_home_route_is_status_ok(self):
        """Test route using client's headers, etc."""
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)

    def test_home_route_context_foo(self):
        """Test that home route has the right context info."""
        response = self.client.get("/")
        self.assertTrue(not response.context["photo"] and response.context["photo_url"])

    def test_home_route_uses_right_templates(self):
        """Check that home page is using the right templates."""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "imagersite/home.html")
        self.assertTemplateUsed(response, "imagersite/base.html")

    def test_login_route_redirects(self):
        """Test that login redirects users."""
        # Put your factories outside your other tests at the top
        new_user = UserFactory.create()
        new_user.save()
        new_user.username = "tralala"
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats",
            })
        self.assertTrue(response.status_code == 302)

    def test_login_route_redirects_to_homepage(self):
        """Test that login redirects users to homepage."""
        # Put your factories outside your other tests at the top
        new_user = UserFactory.create()
        new_user.save()
        new_user.username = "tralala"
        new_user.set_password("tugboats")
        new_user.save()
        response = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats",
            }, follow=True)
        self.assertTrue(response.redirect_chain[0][0] == "/")

    def register_bob(self, follow=False):
        """Create a dummy user named Bob."""
        response = self.client.post("/registration/register/", {
            "username": "bobdobson",
            "email": "bob@dob.son",
            "password1": "tugboats",
            "password2": "tugboats",
        }, follow=follow)
        return response

    def test_can_register_new_user(self):
        """Post request properly filled out creates new user."""
        self.assertTrue(User.objects.count() == 0)
        self.register_bob()
        self.assertTrue(User.objects.count() == 1)

    def test_registered_user_is_inactive(self):
        """Test that a newly registered user is not yet activated."""
        self.register_bob()
        the_user = User.objects.first()
        self.assertFalse(the_user.is_active)

    def test_successful_registration_redirects(self):
        """Test that registration redirects."""
        response = self.register_bob()
        self.assertTrue(response.status_code == 302)

    def test_successful_registration_redirects_to_right_place(self):
        """Test that registration redirects to registration complete page."""
        response = self.register_bob(follow=True)
        self.assertTrue(
            response.redirect_chain[0][0] == '/registration/register/complete/')
