# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username',]

class ProfileSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.id')
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['username', 'profile_image', 'background_image', 'facebook_link']