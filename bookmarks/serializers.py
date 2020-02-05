from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bookmarks.models import Bookmark

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('url', 'description', 'isPublic', 'user')
