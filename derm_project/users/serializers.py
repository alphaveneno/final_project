"""
serializers for user concerns
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ColleagueRequest


# when a User model serializer is required,
# should be placed at the top
class UserSerializer(serializers.ModelSerializer):
    """
    serializer for User
    """

    class Meta:
        """
        Meta: all fields included except password
        """

        model = User
        fields =   ['id', 
                    'last_login',
                    'is_superuser',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'groups',
                    'user_permissions']


class ProxyUserSerializer(UserSerializer):
    """
    To prevent a naming conflict
    between drf-spectacular and drf, because drf
    automatically creates nested serializers
    for UserSerializer, we create a proxy serializer
    """

    class Meta(UserSerializer.Meta):
        """
        new proxy UserSerializer
        """

        fields = UserSerializer.Meta.fields


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile
    """

    user = ProxyUserSerializer()

    class Meta:
        """
        Meta
        """

        model = Profile
        fields = ["user", "image", "slug", "bio", "colleagues"]
        depth = 1

    def create(self, validated_data):
        """
        create profile
        """
        user_data = self.initial_data.get("user")
        profile = Profile(
            **{
                **validated_data,
                "user": User.objects.get(pk=user_data["id"]),
            }
        )
        profile.save()
        return profile

    def update(self, instance, validated_data):
        """
        update profile
        """
        user_data = self.initial_data.get("user")
        instance.image = validated_data.get("image", instance.image)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.colleagues = validated_data.get("colleagues", instance.colleagues)
        instance.user = User.objects.get(pk=user_data["id"])
        instance.save()
        return instance


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Profile list
    """

    class Meta:
        """
        Meta
        """

        model = Profile
        fields = ["user", "image", "slug", "bio", "colleagues"]
        depth = 1


class ColleagueRequestSerializer(serializers.ModelSerializer):
    """
    ColleagueRequest
    """

    to_user = ProxyUserSerializer()
    from_user = ProxyUserSerializer()

    class Meta:
        """
        Meta
        """

        model = ColleagueRequest
        fields = ["to_user", "from_user", "timestamp"]
        depth = 1

    def create(self, validated_data):
        """
        create colleague request
        """
        to_user_data = self.initial_data.get("to_user")
        from_user_data = self.initial_data.get("from_user")
        colquest = ColleagueRequest(
            **{
                **validated_data,
                "to_user": User.objects.get(pk=to_user_data["id"]),
                "from_user": User.objects.get(pk=from_user_data["id"]),
            }
        )
        colquest.save()
        return colquest

    def update(self, instance, validated_data):
        """
        update colleague request
        """
        to_user_data = self.initial_data.get("to_user")
        from_user_data = self.initial_data.get("from_user")
        instance.timestamp = validated_data.get("timestamp", instance.timestamp)
        instance.to_user = User.objects.get(pk=to_user_data["id"])
        instance.from_user = User.objects.get(pk=from_user_data["id"])
        instance.save()
        return instance


class ColleagueRequestListSerializer(serializers.ModelSerializer):
    """
    ColleagueRequest list
    """

    class Meta:
        """
        Meta
        """

        model = ColleagueRequest
        fields = ["to_user", "from_user", "timestamp"]
        depth = 1
