import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "derm_project.settings"
django.setup()

import pytest
from django.contrib.auth.models import User

from pytest_factoryboy import register
from .model_factories import UserFactory, ProfileFactory, ColleagueRequestFactory

register(UserFactory)
register(ProfileFactory)
register(ColleagueRequestFactory)

@pytest.fixture()
def profile_factory():
    """_summary_"""
    def create_profile(
        username: str = "drSimpson",
        password: str = None,
        bio: str = "My name is Dr. Simpson",
        slug: str = "drsimpson",
        email: str = "test@test.com"):
        # colleagues: set = {"nurseGollum", "drGriffin"}):
        return User.objects.create_user(username=username,
                                        password=password,
                                        slug=slug,
                                        bio=bio,
                                        email=email)
                                        # colleagues=colleagues,
                                        # date_joined=date_joined,
                                        # is_superuser=is_superuser)

    return create_profile


@pytest.fixture()
def colleague_request_factory(db):
    """_summary_"""
    def create_colleague_request(
        to_user: str = "drSimpson",
        from_user: str = "nurseGollum",
        date_requested: str = "2023-09-01",
        date_accepted: str = "2023-10-01",
        date_rejected: str = None,
        date_deleted: str = None,
        date_cancelled: str = None,
        accepted: bool = True):
        return User.objects.create_or_get(to_user=to_user,
                                          from_user=from_user,
                                          date_requested=date_requested,
                                          date_accepted=date_accepted,
                                          date_rejected=date_rejected,
                                          date_deleted=date_deleted,
                                          date_cancelled=date_cancelled,
                                          accepted=accepted)

    return create_colleague_request
