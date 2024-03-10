import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from faker import Faker
from users.models import Profile, ColleagueRequest
from faker.providers import BaseProvider
import random

fake = Faker()

#############HELPERS################


class ColleaguesProvider(BaseProvider):
    """_summary_
    """
    def colleagues(self):
        """_summary_
        """
        return random.sample(range(100, 1000), 3)


fake.add_provider(ColleaguesProvider)
######################################

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    """_summary_"""

    class Meta:
        """_summary_"""

        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)
    email = fake.email()
    password = fake.password()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    """
    sets up a profile, essentially a custom user
    """

    class Meta:
        """
        meta
        """

        model = Profile

    user = factory.SubFactory(UserFactory)
    image = fake.image_url()
    slug = fake.word()
    bio = fake.sentence()

    # @factory.post_generation
    # def colleagues(self, create, extracted, **kwargs):
    #     """
    #     to test a django many-to-many relationship
    #     post-generation is necessary
    #     """
    #     if not create:
    #         # Simple build, do nothing.
    #         return

    #     if extracted:
    #         # A list of colleagues were passed in, use them
    #         for colleague in extracted:
    #             self.colleagues.add(colleague)
    #     else:
    #         # No list of colleagues were passed, use the fake.colleagues() method
    #         for colleague in fake.colleagues():
    #             self.colleagues.add(colleague)


UserFactory.profile = factory.RelatedFactory(ProfileFactory, "user")


@factory.django.mute_signals(post_save)
class ColleagueRequestFactory(factory.django.DjangoModelFactory):
    """
    sets up a colleague request
    """

    class Meta:
        """
        meta
        """

        model = ColleagueRequest

    to_user = factory.SubFactory(UserFactory)
    from_user = factory.SubFactory(UserFactory)
    timestamp = fake.date_time_between(start_date="-5m", end_date="now")
