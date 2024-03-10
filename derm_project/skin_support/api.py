"""
APIs related to post concerns
"""
from rest_framework import generics
from rest_framework import mixins

from .models import Post, Comments, Endorse, Vote
from .serializers import (
    PostSerializer,
    PostListSerializer,
    CommentsSerializer,
    CommentsListSerializer,
    EndorseSerializer,
    EndorseListSerializer,
    VoteSerializer,
    VoteListSerializer,
)


class PostDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    PostDetail
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        """
        post
        """
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        get
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        put
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        delete
        """
        return self.destroy(request, *args, **kwargs)


class PostList(generics.ListAPIView):
    """
    Post List
    """

    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class CommentsDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    CommentsDetail
    """

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def post(self, request, *args, **kwargs):
        """
        post
        """
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        get
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        put
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        delete
        """
        return self.destroy(request, *args, **kwargs)


class CommentsList(generics.ListAPIView):
    """
    Comments List
    """

    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer


class EndorseDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    EndorseDetail
    """

    queryset = Endorse.objects.all()
    serializer_class = EndorseSerializer

    def post(self, request, *args, **kwargs):
        """
        post
        """
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        get
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        put
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        delete
        """
        return self.destroy(request, *args, **kwargs)


class EndorseList(generics.ListAPIView):
    """
    Endorse List
    """

    queryset = Endorse.objects.all()
    serializer_class = EndorseListSerializer


class VoteDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    VoteDetail
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def post(self, request, *args, **kwargs):
        """
        post
        """
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        get
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        put
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        delete
        """
        return self.destroy(request, *args, **kwargs)


class VoteList(generics.ListAPIView):
    """
    Vote List
    """

    queryset = Vote.objects.all()
    serializer_class = VoteListSerializer
