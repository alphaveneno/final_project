"""
models for Post, Comment, and Endorse
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """
    'history' is the patient's history
    the author must post images and tags for the post
    to make it searchable
    The Comments model (see below) is for recording
    the thread of conversation
    """

    age = models.CharField(max_length=3, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    ethnicity = models.CharField(max_length=25, blank=True)
    history = models.TextField(blank=True)
    country = models.CharField(max_length=25, blank=True)
    skin_location = models.CharField(max_length=25, blank=True)
    provdx = models.CharField(max_length=50, blank=True)
    ddx1 = models.CharField(max_length=50, blank=True)
    ddx2 = models.CharField(max_length=50, blank=True)
    pic1 = models.ImageField(upload_to="pics/")
    pic2 = models.ImageField(upload_to="pics/", default="pics/blank.png")
    pic3 = models.ImageField(upload_to="pics/", default="pics/blank.png")
    date_posted = models.DateTimeField(default=timezone.now)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.history)

    def get_absolute_url(self):
        """
        gets the id of the post, which is 'pk', for example, "1",
        then goes to urls.py to find the url path with name 'post-detail':
        path("post/<int:pk>/", views.post_detail, name="post-detail"),
        then returns the complete url for the post:
        "/post/1"
        """
        return reverse("post-detail", kwargs={"pk": self.pk})


class Comments(models.Model):
    """
    'comment is an unlimited TextField
    'details' is essentially an alias for 'comments'
    """

    post = models.ForeignKey(Post, related_name="details", on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name="details", on_delete=models.CASCADE)
    provdx = models.CharField(max_length=50, blank=True)
    ddx1 = models.CharField(max_length=50, blank=True)
    ddx2 = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    comment_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=100, blank=True)

    def vote(self):
        """
        returns the user_ids of upvotes
        for a particular comment
        """
        querySet = Vote.objects.filter(comment_id=self)
        id_list = [item.user_id for item in querySet]
        return id_list


class Endorse(models.Model):
    """
    an 'endorse' is a pairing of a user to a post, created in this model
    """

    user = models.ForeignKey(User, related_name="endorses", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="endorses", on_delete=models.CASCADE)


class Vote(models.Model):
    """
    'vote' is a pairing of a user to a comment, created in this model
    this model imported into users/models.py
    """

    user = models.ForeignKey(User, related_name="votes", on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comments, related_name="votes", on_delete=models.CASCADE
    )
