"""
crispy forms for posts and comments
"""
from django import forms
from .models import Comments, Post


class NewPostForm(forms.ModelForm):
    """
    new posts
    """

    class Meta:
        """
        meta
        """

        model = Post
        fields = [
            "age",
            "gender",
            "ethnicity",
            "history",
            "country",
            "skin_location",
            "provdx",
            "ddx1",
            "ddx2",
            "pic1",
            "pic2",
            "pic3",
            "tags",
        ]


class NewCommentForm(forms.ModelForm):
    """
    new comments
    """

    class Meta:
        """
        meta
        """

        model = Comments
        fields = ["provdx", "ddx1", "ddx2", "comment", "tags"]
