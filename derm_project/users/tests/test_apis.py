from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from users.models import Profile

# Comment: the issue with testing the built-in classes of django
# and django-rest-framework is - usually - it is the functionality of
# these libraries that is actually being tested,
# not the code written by the developer.
# The exception: any customized code added by the developer should be tested


class ProfileDetailAPITest(TestCase):
    """
    test the profile detail API
    """

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username="testuser1", password="_skin999TEST_"
        )
        # self.user2 = User.objects.create_user(
        #     username="testuser2", password="_skin999TEST_"
        # )
        self.profile, created = Profile.objects.get_or_create(user=self.user1)
        self.client.login(username="testuser1", password="_skin999TEST_")
        self.url = reverse("profile_api", kwargs={"pk": self.user1.id})

    def test_get_profile(self):
        """
        test GET profile
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["id"], self.user1.id)

    def test_update_profile(self):
        """
        test PUT profile
        """
        pass
        # new_data = {
        #     "user": {"username": self.user2.username, "password": self.user2.password},
        #     "slug": "testuser1",
        #     "bio": "test bio of testuser1",
        # }
        # response = self.client.put(self.url, new_data, format="json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.profile.refresh_from_db()
        # self.assertEqual(self.profile.slug, "testuser1")
        # self.assertEqual(self.profile.user.username, self.user2.username)

    def test_delete_profile(self):
        """
        test DELETE profile
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())
