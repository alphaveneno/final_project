"""
testing with factory boy
"""
import json
from django.urls import reverse

from rest_framework.test import APITestCase

# must use 'import *', NOT just 'import PostFactory, CommentsFactory'
from .model_factories import *
from .serializers import *


class PostSerializerTest(APITestCase):
    """
    tests PostSerializer
    """

    post1 = None
    postserializer = None

    def setUp(self):
        """
        setup post serializer tests
        """
        self.post1 = PostFactory.create()
        self.postserializer = PostSerializer(instance=self.post1)

    # necessary to tear down ALL models and reset
    # after running a fixture
    def tearDown(self):
        """
        teardown post serializer tests
        """
        Post.objects.all().delete()
        PostFactory.reset_sequence(0)
        Comments.objects.all().delete()
        CommentsFactory.reset_sequence(0)
        User.objects.all().delete()
        UserFactory.reset_sequence(0)

    def test_postSerialize_keys_fail(self):
        """
        tests that these strings are not in the keyset
        """
        data = self.postserializer.data
        self.assertNotEqual(set(data.keys()), set(["aaa", "bbb", "ccc", "ddd", "eee"]))

    def test_postSerialize_keys_pass(self):
        """
        tests that keyset matches Post settings
        """
        data = self.postserializer.data
        self.assertEqual(
            set(data.keys()),
            set(["history", "pic", "date_posted", "user_name", "tags"]),
        )

    def test_postSerializer_data_fail(self):
        """
        check that serializer does not return 'rash'
        """
        data = self.postserializer.data
        self.assertNotEqual(data["history"], "rash")

    def test_postSerializer_data_pass(self):
        """
        check that serializer returns the default value from the PostFactory
        """
        data = self.postserializer.data
        self.assertEqual(data["history"], "psoriasis")


class CommentsSerializerTest(APITestCase):
    """
    tests CommentsSerializer
    """

    comments1 = None
    commentsserializer = None

    def setUp(self):
        """
        setup comments serializer tests
        """
        self.user = UserFactory()
        self.post = PostFactory(user_name=self.user)

        # self.post and self.comments1 must have the exact same self.user object
        # o/w self.comments1 is rejected as an integrity error
        self.comments1 = CommentsFactory.create(username=self.user, post=self.post)
        self.commentsserializer = CommentsSerializer(instance=self.comments1)

    def tearDown(self):
        """
        teardown comments serializer tests
        """
        Post.objects.all().delete()
        PostFactory.reset_sequence(0)
        Comments.objects.all().delete()
        CommentsFactory.reset_sequence(0)
        User.objects.all().delete()
        UserFactory.reset_sequence(0)

    def test_commentsSerialize_keys_fail(self):
        """
        tests that these strings are not in the keyset
        """
        data = self.commentsserializer.data
        self.assertNotEqual(set(data.keys()), set(["aaa", "bbb", "ccc", "ddd"]))

    def test_commentsSerialize_keys_pass(self):
        """
        tests that keyset matches Comments settings
        """
        data = self.commentsserializer.data
        self.assertEqual(
            set(data.keys()), set(["post", "username", "comment", "comment_date"])
        )

    def test_commentsSerializer_data_fail(self):
        """
        check that serializer does not return ''
        """
        data = self.commentsserializer.data
        self.assertNotEqual(data["comment"], "")

    def test_commentsSerializer_data_pass(self):
        """
        check that serializer returns the default value from the CommentsFactory
        """
        data = self.commentsserializer.data
        self.assertEqual(data["comment"], "")


class PostTest(APITestCase):
    """
    tests Post
    """

    post1 = None
    post2 = None

    def setUp(self):
        """
        setup post test
        """
        self.post1 = PostFactory.create(pk=1)
        self.url_post1 = reverse("post_api", kwargs={"pk": "1"})
        # self.post2 = PostFactory.create(pk=2, history='456testing', tags = "aTest")
        # self.url_post2 = reverse('post_api', kwargs = {'pk':'2'})

    def tearDown(self):
        """
        teardown post test
        """
        Post.objects.all().delete()
        PostFactory.reset_sequence(0)
        Comments.objects.all().delete()
        CommentsFactory.reset_sequence(0)
        User.objects.all().delete()
        UserFactory.reset_sequence(0)

    def test_post_fail_url(self):
        """
        tests that false url input is incorrect
        """
        response = self.client.get(self.url_post1, format="json")
        response.render()
        self.assertNotEqual(response.status_code, 204)

    def test_post_fail_field(self):
        """
        tests that false field name is incorrect
        """
        response = self.client.get(self.url_post1, format="json")
        response.render()
        data = json.loads(response.content)
        self.assertFalse("post" in data)

    def test_post_fail_data(self):
        """
        tests that false data is incorrect
        """
        response = self.client.get(self.url_post1, format="json")
        response.render()
        data = json.loads(response.content)
        self.assertNotEqual(data["tags"], "")

    def test_post_pass(self):
        """
        the pass tests which match
        the three fail tests above
        are all run here
        """
        response = self.client.get(self.url_post1, format="json")
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue("tags" in data)
        self.assertEqual(data["tags"], "")


class CommentsTest(APITestCase):
    """
    tests Comments
    """

    comments1 = None
    comments2 = None

    def setUp(self):
        """
        setup comments tests
        """
        self.user = UserFactory()
        self.post = PostFactory(user_name=self.user)

        # self.post and self.comments1 must have the exact same self.user object
        self.comments1 = CommentsFactory.create(
            pk=1, username=self.user, post=self.post
        )
        self.url_comments1 = reverse("comment_api", kwargs={"pk": "1"})
        # self.comments2 = CommentsFactory.create(comments="testing123")
        # self.url_comments2 = reverse('comment_api', kwargs = {'pk': '2'})

    def tearDown(self):
        """
        teardown comments tests
        """
        Post.objects.all().delete()
        PostFactory.reset_sequence(0)
        Comments.objects.all().delete()
        CommentsFactory.reset_sequence(0)
        User.objects.all().delete()
        UserFactory.reset_sequence(0)

    def test_comments_url_fail(self):
        """
        tests that comments_url is correct and does not return 404
        """
        response = self.client.get(self.url_comments1, format="json")
        response.render()
        self.assertNotEqual(response.status_code, 404)

    def test_comments_field_fail(self):
        """
        tests that false field name is incorrect
        """
        response = self.client.get(self.url_comments1, format="json")
        response.render()
        data = json.loads(response.content)
        self.assertFalse("remarks" in data)

    def test_comments_data_fail(self):
        """
        tests that false data is incorrect
        """
        response = self.client.get(self.url_comments1, format="json")
        response.render()
        data = json.loads(response.content)
        self.assertNotEqual(data["comment"], "")

    def test_comments_pass(self):
        """
        tests if all input matches data from Commentsfactory
        """
        response = self.client.get(self.url_comments1, format="json")
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue("comment" in data)
        self.assertEqual(data["comment"], "")
