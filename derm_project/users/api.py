"""
APIs related to users concerns
"""
from rest_framework import generics
from rest_framework import mixins

from .models import Profile, ColleagueRequest
from .serializers import (
    ProfileSerializer,
    ProfileListSerializer,
    ColleagueRequestSerializer,
    ColleagueRequestListSerializer,
)


class ProfileDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    ProfileDetail
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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


class ProfileList(generics.ListAPIView):
    """
    Profile List
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer


class ColleagueRequestDetail(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    ColleagueRequestDetail
    """

    queryset = ColleagueRequest.objects.all()
    serializer_class = ColleagueRequestSerializer

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


class ColleagueRequestList(generics.ListAPIView):
    """
    ColleagueRequest List
    """

    queryset = ColleagueRequest.objects.all()
    serializer_class = ColleagueRequestListSerializer
