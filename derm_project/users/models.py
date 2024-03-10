"""
Users module: profile model contains info to supplement
the built-in Django User model
the two models have a OneToOne match
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField


class Profile(models.Model):
    """
    profile model: users' names are matched OneToOne
    to their entry in the built-in User model
    'colleagues' are a ManyToMany relationship
    in the Profile model
    """

    # Two Scoops of Django recommends using settings.AUTH_USER_MODEL
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics/")
    slug = AutoSlugField(populate_from="user")
    bio = models.CharField(max_length=255, blank=True)
    colleagues = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        """
        using a slug to create the path to the user profile
        """
        return f"/users/{self.slug}"


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    """
    pairs the profile to the matching user,
    creates a new profile if necessary
    """
    if created:
        try:
            Profile.objects.create(user=instance)
        except [ValueError, TypeError, RuntimeError]:
            pass


post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)


class ColleagueRequest(models.Model):
    """
    colleague requests are represented
    as pairs of two different foreign keys,
    paired as OneToOne with this model
    """

    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_user", on_delete=models.CASCADE
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="from_user", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user}, to {self.to_user}"
