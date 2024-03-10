import pytest
from django.contrib.auth.models import User
# from .factories.conftest import profile_factory
from .factories.model_factories import ProfileFactory
import re

# requires pytest-django
@pytest.fixture()
def user_1(db):
    """
    user_1
    """
    return User.objects.create_user(username="user_1",
                                    email="user_1@example.com",
                                    password="password")


@pytest.mark.django_db
def test_profile():
    """
    test_profile
    """
    # user_1 = user_1
    profile = ProfileFactory.create()
    assert isinstance(profile.user.username, str)
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    assert re.match(email_regex, profile.user.email)
    assert isinstance(profile.slug, str)
    assert " " in profile.bio


def test_ColleagueRequest():
    """
    test colleagues
    """
    pass
