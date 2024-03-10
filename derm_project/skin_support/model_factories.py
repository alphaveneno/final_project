"""
model factories
"""
import factory

# from django.test import TestCase
# from django.core.files import File
from django.contrib.auth.models import User

from .models import Post, Comments, Endorse


class UserFactory(factory.django.DjangoModelFactory):
    """
    sets up a username
    """

    username = "drSimpson"

    class Meta:
        """
        meta
        """

        model = User


class PostFactory(factory.django.DjangoModelFactory):
    """
    creates a Post object from data taken from database
    """

    pic = "http://localhost:8000/media/path/media/pics/psoriasis.jpg"
    description = "psoriasis"
    date_posted = "2023-02-19T14:32:36.752250Z"
    user_name = factory.SubFactory(UserFactory)
    tags = "psoriasis"

    class Meta:
        """
        meta
        """

        model = Post


class CommentsFactory(factory.django.DjangoModelFactory):
    """
    creates a Comments object from data taken from database
    """

    post = factory.SubFactory(PostFactory)

    # in tests.py this will be replaced with
    # the UseFactory object found in 'post'
    username = factory.SubFactory(UserFactory)
    comment = "This looks like psoriasis"
    comment_date = "2023-02-19T14:34:03.188013Z"

    class Meta:
        """
        meta
        """

        model = Comments


class EndorseFactory(factory.django.DjangoModelFactory):
    """
    creates a Endorse object from data taken from database
    """

    post = factory.SubFactory(PostFactory)
    username = factory.SubFactory(UserFactory)

    class Meta:
        """
        meta
        """

        model = Endorse
