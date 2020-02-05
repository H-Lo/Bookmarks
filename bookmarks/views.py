from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from rest_framework import viewsets

from bookmarks.models import Bookmark
from bookmarks.serializers import UserSerializer, BookmarkSerializer


def home(request):
    return HttpResponse('Hello, World!')


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    def get_queryset(self):
        queryset = Bookmark.objects.all()
        scope = self.request.query_params.get('scope', None)
        if scope == 'all' :
            return queryset.exclude(~Q(user = self.request.user.id), isPublic = False)
        if scope == 'others' :
            return queryset.exclude(user = self.request.user).exclude(isPublic = False)
        # show only mine
        return queryset.filter(user = self.request.user.id)
