from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from bookmarks import views

router = routers.DefaultRouter()
router.register('users',     views.UserViewSet,     basename='user')
router.register('bookmarks', views.BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
