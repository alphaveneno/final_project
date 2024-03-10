"""
serializers for post concerns
"""

from users.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comments, Endorse, Vote


class PostUserSerializer(UserSerializer):
    """
    To prevent a naming conflict
    between drf-spectacular and drf, because drf
    automatically creates nested serializers
    for UserSerializer, we create a new serializer
    """

    class Meta(UserSerializer.Meta):
        """
        new proxy UserSerializer
        """

        fields = UserSerializer.Meta.fields


class PostSerializer(serializers.ModelSerializer):
    """
    Post
    """

    user_name = PostUserSerializer()

    class Meta:
        """
        Meta
        """

        model = Post
        fields = [
            "pic1",
            "pic2",
            "pic3",
            "age",
            "gender",
            "ethnicity",
            "history",
            "country",
            "skin_location",
            "provdx",
            "ddx1",
            "ddx2",
            "date_posted",
            "user_name",
            "tags",
        ]
        depth = 1

    def create(self, validated_data):
        """
        create post
        """
        user_data = self.initial_data.get("user_name")
        post = Post(
            **{
                **validated_data,
                "user_name": User.objects.get(pk=user_data["id"]),
            }
        )
        post.save()
        return post

    def update(self, instance, validated_data):
        """
        update post
        """
        user_data = self.initial_data.get("user_name")
        instance.age = validated_data.get("age", instance.age)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.ethnicity = validated_data.get("ethnicity", instance.ethnicity)
        instance.country = validated_data.get("country", instance.country)
        instance.skin_location = validated_data.get(
            "skin_location", instance.skin_location
        )
        instance.provdx = validated_data.get("provdx", instance.provdx)
        instance.ddx1 = validated_data.get("ddx1", instance.ddx1)
        instance.ddx2 = validated_data.get("ddx2", instance.ddx2)
        instance.pic1 = validated_data.get("pic", instance.pic1)
        instance.pic2 = validated_data.get("pic", instance.pic2)
        instance.pic3 = validated_data.get("pic", instance.pic3)
        instance.history = validated_data.get("history", instance.history)
        instance.date_posted = validated_data.get("date_posted", instance.date_posted)
        instance.tags = validated_data.get("tags", instance.tags)
        instance.user_name = User.objects.get(pk=user_data["id"])
        instance.save()
        return instance


class ProxyPostSerializer(PostSerializer):
    """
    To prevent a naming conflict
    between drf-spectacular and drf, because drf
    automatically creates nested serializers
    for PostSerializer, we create a proxy serializer
    """

    class Meta(PostSerializer.Meta):
        """
        new proxy Post serializer
        """

        fields = PostSerializer.Meta.fields


class PostListSerializer(serializers.ModelSerializer):
    """
    Post: user_name does not include password
    """

    user_name = PostUserSerializer(read_only=True)

    class Meta:
        """
        Meta
        """

        model = Post
        fields = fields = [
            "pic1",
            "pic2",
            "pic3",
            "age",
            "gender",
            "ethnicity",
            "history",
            "country",
            "skin_location",
            "provdx",
            "ddx1",
            "ddx2",
            "date_posted",
            "user_name",
            "tags",
        ]
        depth = 1


class CommentsSerializer(serializers.ModelSerializer):
    """
    Comments
    """

    username = PostUserSerializer()
    post = ProxyPostSerializer()

    class Meta:
        """
        Meta
        """

        model = Comments
        fields = ["post", "username", "comment", "comment_date"]
        # depth = 1

    def create(self, validated_data):
        """
        create comment
        """
        user_data = self.initial_data.get("username")
        post_data = self.initial_data.get("post")
        comment = Comments(
            **{
                **validated_data,
                "username": User.objects.get(pk=user_data["id"]),
                "post": Post.objects.get(pk=post_data["id"]),
            }
        )
        comment.save()
        return comment

    def update(self, instance, validated_data):
        """
        update comment
        """
        user_data = self.initial_data.get("username")
        instance.post = validated_data.get("post", instance.post)
        instance.username = User.objects.get(pk=user_data["id"])
        instance.comment = validated_data.get("comment", instance.comment)
        instance.comment_date = validated_data.get(
            "comment_date", instance.comment_date
        )
        instance.save()
        return instance


class ProxyCommentsSerializer(CommentsSerializer):
    """
    To prevent a naming conflict
    between drf-spectacular and drf, because drf
    automatically creates nested serializers
    for CommentsSerializer, we create a proxy serializer
    """

    class Meta(CommentsSerializer.Meta):
        """
        new proxy CommentsSerializer
        """

        fields = CommentsSerializer.Meta.fields


class CommentsListSerializer(serializers.ModelSerializer):
    """
    Comments list: username does not include password
    """

    username = PostUserSerializer(read_only=True)

    class Meta:
        """
        Meta
        """

        model = Comments
        fields = ["post", "username", "comment", "comment_date"]
        depth = 1


class EndorseSerializer(serializers.ModelSerializer):
    """
    endorsements of comments
    """

    user = PostUserSerializer()
    post = ProxyPostSerializer()

    class Meta:
        """
        Meta
        """

        model = Endorse
        fields = ["post", "user"]
        depth = 1

    def create(self, validated_data):
        """
        create a endorse
        """
        user_data = self.initial_data.get("user")
        post_data = self.initial_data.get("post")
        endorse = Endorse(
            **{
                **validated_data,
                "user": User.objects.get(pk=user_data["id"]),
                "post": Post.objects.get(pk=post_data["id"]),
            }
        )
        endorse.save()
        return endorse

    def update(self, instance, validated_data):
        """
        update a endorse
        """
        user_data = self.initial_data.get("user")
        post_data = self.initial_data.get("post")
        instance.post = Post.objects.get(pk=post_data["id"])
        instance.post = validated_data.get("post", instance.post)
        instance.user = User.objects.get(pk=user_data["id"])
        instance.user = validated_data.get("user", instance.user)
        instance.save()
        return instance


class EndorseListSerializer(serializers.ModelSerializer):
    """
    Endorse list: user does not include password
    """

    user = PostUserSerializer(read_only=True)

    class Meta:
        """
        Meta
        """

        model = Endorse
        fields = ["post", "user"]
        depth = 1


class VoteSerializer(serializers.ModelSerializer):
    """
    upvotes
    """

    user = PostUserSerializer()
    comment = ProxyCommentsSerializer()

    class Meta:
        """
        Meta
        """

        model = Vote
        fields = ["comment", "user"]
        depth = 1

    def create(self, validated_data):
        """
        create a vote
        """
        user_data = self.initial_data.get("user")
        comments_data = self.initial_data.get("comments")
        vote = Vote(
            **{
                **validated_data,
                "user": User.objects.get(pk=user_data["id"]),
                "comments": Comments.objects.get(pk=comments_data["id"]),
            }
        )
        vote.save()
        return vote

    def update(self, instance, validated_data):
        """
        update a vote
        """
        user_data = self.initial_data.get("user")
        comments_data = self.initial_data.get("comments")
        instance.comments = Comments.objects.get(pk=comments_data["id"])
        instance.comments = validated_data.get("comments", instance.comments)
        instance.user = User.objects.get(pk=user_data["id"])
        instance.user = validated_data.get("user", instance.user)
        instance.save()
        return instance


class VoteListSerializer(serializers.ModelSerializer):
    """
    Vote list: user does not include password
    """

    user = PostUserSerializer(read_only=True)

    class Meta:
        """
        Meta
        """

        model = Vote
        fields = ["comment", "user"]
        depth = 1
