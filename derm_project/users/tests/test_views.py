from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm
from users.models import Profile, ColleagueRequest
from ..views import *


class MyProfileViewTest(TestCase):
    """
    test my_profile view
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="drSimpson", password="goldsmiths123")
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.url = reverse(
            "my_profile"
        )  # replace 'my_profile' with the actual name of the view

    def test_redirect_if_not_logged_in(self):
        """
        if not logged in, redirect to login page
        """
        response = self.client.get(self.url)
        self.assertRedirects(
            response, "/?next=/my-profile/")

        # replace '/login/' with the actual login url

    def test_no_redirect_if_logged_in(self):
        """
        sucessful login
        """
        self.client.login(username="drSimpson", password="goldsmiths123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_context_if_no_colleagues_and_no_requests(self):
        """
        if no colleagues and no requests, test context
        """
        self.client.login(username="drSimpson", password="goldsmiths123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["u"], self.user)
        self.assertEqual(response.context["button_status"], "not_colleague")
        self.assertEqual(list(response.context["colleague_list"]), [])
        self.assertEqual(list(response.context["sent_colleague_requests"]), [])
        self.assertEqual(list(response.context["rec_colleague_requests"]), [])
        self.assertEqual(response.context["post_count"], 0)

    def test_context_if_colleagues_and_requests(self):
        """
        add another user and test context
        """
        other_user = User.objects.create_user(
            username="otherUser", password="password123"
        )
        other_profile, created = Profile.objects.get_or_create(user=other_user)
        self.profile.colleagues.add(other_profile)
        sent_request = ColleagueRequest.objects.create(from_user=self.user,
                                                       to_user=other_user)
        received_request = ColleagueRequest.objects.create(from_user=other_user,
                                                           to_user=self.user)
        Post.objects.create(user_name=self.user, provdx="Test post")
        self.client.login(username="drSimpson", password="goldsmiths123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["u"], self.user)
        self.assertEqual(response.context["button_status"], "not_colleague")
        self.assertEqual(list(response.context["colleague_list"]), [other_profile])
        self.assertEqual(list(response.context["sent_colleague_requests"]), [sent_request])
        self.assertEqual(
            list(response.context["rec_colleague_requests"]), [received_request]
        )
        self.assertEqual(response.context["post_count"], 1)


class EditProfileViewTest(TestCase):
    """
    test edit profile view
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.url = reverse(
            "edit_profile"
        )

    def test_get_edit_profile(self):
        """
        test GET request
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/edit_profile.html")
        self.assertIsInstance(response.context["u_form"], UserUpdateForm)
        self.assertIsInstance(response.context["p_form"], ProfileUpdateForm)

    def test_post_edit_profile(self):
        """
        test POST request
        """
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            self.url,
            {
                "username": "newusername",
                "email": "newemail@example.com",
                "image": "default.png",
            },
        )
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.profile.image, "default.png")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("my_profile")
        )


class RegisterViewTest(TestCase):
    """
    test register view
    """
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_get_register(self):
        """
        test GET request
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertIsInstance(response.context["form"], UserRegisterForm)

    def test_post_register(self):
        """
        test POST request
        """
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "_skin999TEST_",
                "password2": "_skin999TEST_",
            },
        )
        if response.context and 'form' in response.context:
            print(response.context['form'].errors)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "newuser")
        self.assertEqual(User.objects.first().email, "newuser@example.com")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("login")
        )

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SearchUsersViewTest(TestCase):
    """
    test search users view
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="_skin999TEST_"
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="_skin888TEST_"
        )
        self.client.login(username="testuser1",
                          password="_skin999TEST_")
        self.url = reverse(
            "search_users"
        )

    def test_search_users(self):
        """
        test search users for testuser2
        """
        response = self.client.get(self.url, {"q": "testuser2"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/search_users.html")
        self.assertEqual(list(response.context["users"]), [self.user2])

    def test_search_users_no_results(self):
        """
        test search users with no results
        """
        response = self.client.get(self.url, {"q": "nonexistentuser"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/search_users.html")
        self.assertQuerysetEqual(response.context["users"], [])


class ProfileViewTest(TestCase):
    """
    test profile view
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="_skin999TEST_"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="_skin888TEST_"
        )
        self.profile1, created1 = Profile.objects.get_or_create(
            user=self.user1, slug="testuser1"
        )
        self.profile2, created2 = Profile.objects.get_or_create(
            user=self.user2, slug="testuser2"
        )
        self.client.login(username="testuser1", password="_skin999TEST_")
        self.url = reverse("profile_view", kwargs={"slug": "testuser2"})

    def test_profile_view(self):
        """
        test profile view
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.context["u"], self.user2)
        self.assertEqual(response.context["button_status"], "not_colleague")
        self.assertEqual(list(response.context["colleagues_list"]), [])
        self.assertEqual(list(response.context["sent_colleague_requests"]), [])
        self.assertEqual(list(response.context["rec_colleague_requests"]), [])
        self.assertEqual(response.context["post_count"](), 0)


class DeleteColleagueViewTest(TestCase):
    """_summary_
    test deletion of colleague, show colleague is gone
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="_skin999TEST_"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="_skin888TEST_"
        )
        self.profile1, created1 = Profile.objects.get_or_create(
            user=self.user1, slug="testuser1"
        )
        self.profile2, created2 = Profile.objects.get_or_create(
            user=self.user2, slug="testuser2"
        )
        self.profile1.colleagues.add(self.profile2)
        self.profile2.colleagues.add(self.profile1)
        self.client.login(username="testuser1", password="_skin999TEST_")
        self.url = reverse("delete_colleague", kwargs={"id": self.profile2.id})

    def test_delete_colleague(self):
        """
        test delete colleague
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.profile1.colleagues.filter(id=self.profile2.id).exists())
        self.assertFalse(self.profile2.colleagues.filter(id=self.profile1.id).exists())


class AcceptColleagueRequestViewTest(TestCase):
    """
    test colleague request acceptance
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="_skin999TEST_"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="_skin888TEST_"
        )
        self.profile1, created1 = Profile.objects.get_or_create(
            user=self.user1, slug="testuser1"
        )
        self.profile2, created2 = Profile.objects.get_or_create(
            user=self.user2, slug="testuser2"
        )
        self.colleague_request = ColleagueRequest.objects.create(
            from_user=self.user2, to_user=self.user1
        )
        self.client.login(username="testuser1", password="_skin999TEST_")
        self.url = reverse(
            "accept_colleague_request", kwargs={"id": self.user2.id}
        ) 

    def test_accept_colleague_request(self):
        """
        test colleague request acceptance
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.profile1.colleagues.filter(id=self.profile2.id).exists())
        self.assertTrue(self.profile2.colleagues.filter(id=self.profile1.id).exists())
        self.assertFalse(
            ColleagueRequest.objects.filter(id=self.colleague_request.id).exists()
        )


class DeleteColleagueRequestViewTest(TestCase):
    """
    test deletion of colleague request
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="_skin999TEST_"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="_skin888TEST_"
        )
        self.profile1, created1 = Profile.objects.get_or_create(
            user=self.user1, slug="testuser1"
        )
        self.profile2, created2 = Profile.objects.get_or_create(
            user=self.user2, slug="testuser2"
        )
        self.colleague_request = ColleagueRequest.objects.create(
            from_user=self.user2, to_user=self.user1
        )
        self.client.login(username="testuser1", password="_skin999TEST_")
        self.url = reverse("delete_colleague_request", kwargs={"id": self.user2.id})

    def test_delete_colleague_request(self):
        """
        test deletion of colleague request
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ColleagueRequest.objects.filter(id=self.colleague_request.id).exists()
        )


class CancelColleagueRequestViewTest(TestCase):
    """
    test cancellation of colleague request
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='_skin999TEST_')
        self.user2 = User.objects.create_user(username='testuser2', password='_skin888TEST_')
        self.profile1, created1 = Profile.objects.get_or_create(user=self.user1, slug='testuser1')
        self.profile2, created2 = Profile.objects.get_or_create(user=self.user2, slug='testuser2')
        self.colleague_request = ColleagueRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.login(username='testuser1', password='_skin999TEST_')
        self.url = reverse('cancel_colleague_request', kwargs={'id': self.user2.id})

    def test_cancel_colleague_request(self):
        """
        test cancellation of colleague request
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ColleagueRequest.objects.filter(id=self.colleague_request.id).exists())


class SendColleagueRequestViewTest(TestCase):
    """
    test sending a request to be colleagues
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='_skin999TEST_')
        self.user2 = User.objects.create_user(username='testuser2', password='_skin888TEST_')
        self.profile1, created1 = Profile.objects.get_or_create(user=self.user1, slug='testuser1')
        self.profile2, created2 = Profile.objects.get_or_create(user=self.user2, slug='testuser2')
        self.client.login(username='testuser1', password='_skin999TEST_')
        self.url = reverse('send_colleague_request', kwargs={'id': self.user2.id})  # replace 'send_colleague_request' with the actual name of the view

    def test_send_colleague_request(self):
        """
        test sending a request to be colleagues
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ColleagueRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())


class ColleagueListViewTest(TestCase):
    """
    test colleague list view
    """
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="_skin999TEST_"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="_skin888TEST_"
        )
        self.profile1, created1 = Profile.objects.get_or_create(
            user=self.user1, slug="testuser1"
        )
        self.profile2, created2 = Profile.objects.get_or_create(
            user=self.user2, slug="testuser2"
        )
        self.profile1.colleagues.add(self.profile2)
        self.client.login(username="testuser1", password="_skin999TEST_")
        self.url = reverse(
            "colleague_list"
        )

    def test_colleague_list(self):
        """
        test colleague list view
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser2")


class UsersListViewTest(TestCase):
    """
    test view of list of possible colleague candidates
    """

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser1', password='_skin999TEST_')
        self.user2 = User.objects.create_user(username='testuser2', password='_skin888TEST_')
        self.profile1, created1 = Profile.objects.get_or_create(user=self.user1)
        self.profile2, created2 = Profile.objects.get_or_create(user=self.user2)
        self.client.login(username='testuser1', password='_skin999TEST_')
        self.url = reverse('users_list')

    def test_users_list(self):
        """
        test view of list of possible colleague candidates
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser2')

