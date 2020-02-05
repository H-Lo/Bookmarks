import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from rest_framework.reverse import reverse

USERNAME1 = '__test1__'
PASSWORD1 = 'test1'
EMAIL1    = 'info@thevegcat.com'
NEW_EMAIL = 'hlo@thevegcat.com'

USERNAME2 = '__test2__'
PASSWORD2 = 'test2'
EMAIL2    = 'info@vegcook.net'


class CreateUpdateDeleteUserTestCase(TestCase):

    client = Client()

    def runTest(self):
        lenBefore = TestUtil.getListLength(self, 'user-list')

        TestUtil.addUser(self, USERNAME1, EMAIL1, PASSWORD1)
        lenAfter = TestUtil.getListLength(self, 'user-list')
        assert lenAfter - lenBefore == 1, "Failed while trying to create test user"

        # fetch the user to get the ID
        userFromDb = User.objects.get(username = USERNAME1)

        TestUtil.updateEmail(self, userFromDb, NEW_EMAIL)
        userAfterUpdate = TestUtil.getUser(self, userFromDb.id)
        assert userAfterUpdate["email"] == NEW_EMAIL, 'Failed while trying to update test user'

        TestUtil.deleteUser(self, userFromDb.id)
        finalLen = TestUtil.getListLength(self, 'user-list')
        assert finalLen == lenBefore, "Failed while trying to delete test user"


class UserLoginTestCase(TestCase):

    client = Client()

    def runTest(self):
        TestUtil.addUser(self, USERNAME1, EMAIL1, PASSWORD1)

        userFromDb = User.objects.get(username = USERNAME1)
        assert userFromDb.username == USERNAME1, 'User not created as expected'
        assert userFromDb.email    == EMAIL1,    'User not created as expected'

        usersCount = TestUtil.getListLength(self, 'user-list')
        assert usersCount == 1, 'Could not create user'

        logged_in = self.client.login( username = USERNAME1, password = PASSWORD1 )
        assert logged_in == True, 'Could not log in'

        self.client.logout()


class CreateBookmarksTestCase(TestCase):

    client = Client()

    def runTest(self):

        user1 = TestUtil.addUser(self, USERNAME1, EMAIL1, PASSWORD1)
        user2 = TestUtil.addUser(self, USERNAME2, EMAIL2, PASSWORD2)

        assert TestUtil.getListLength(self, 'user-list') == 2, 'Could not create user'

        loggedIn = self.client.login( username = USERNAME1, password = PASSWORD1 )
        assert loggedIn == True, 'Could not log in'

        TestUtil.createBookmark(self, user=user1, isPublic=True, url="https://thevegcat.com/", description="The best vegan catalog in the world")
        assert TestUtil.getListLength(self, 'bookmark-list')                  == 1, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=all')    == 1, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=others') == 0, "Failed while trying to add bookmarks"

        TestUtil.createBookmark(self, user=user1, isPublic=False, url="https://vegcook.net/", description="The best vegan recipes in the world")
        assert TestUtil.getListLength(self, 'bookmark-list')                  == 2, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=all')    == 2, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=others') == 0, "Failed while trying to add bookmarks"

        TestUtil.createBookmark(self, user=user2, isPublic=True, url="https://malizwrk.net/", description="The best model in the world")
        assert TestUtil.getListLength(self, 'bookmark-list')                  == 2, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=all')    == 3, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=others') == 1, "Failed while trying to add bookmarks"

        TestUtil.createBookmark(self, user=user2, isPublic=False, url="https://horvoje.net/", description="Nothing special")
        assert TestUtil.getListLength(self, 'bookmark-list')                  == 2, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=all')    == 3, "Failed while trying to add bookmarks"
        assert TestUtil.getListLength(self, 'bookmark-list', '?scope=others') == 1, "Failed while trying to add bookmarks"

# ------------------------------------------------------------------------------------------------

class TestUtil:

    def addUser(self, username, email, password):
        TestUtil.createUserNoPassword(self, username, email)
        TestUtil.setPassword(self, username, password)
        userFromDb = User.objects.get(username=username)
        assert userFromDb.username == username, 'User not created as expected'
        assert userFromDb.email    == email,    'User not created as expected'
        return userFromDb

    def createUserNoPassword(self, username, email):
        resp = self.client.post(
            reverse('user-list'),
            {
                "username" : username,
                "email"    : email,
                "groups" : []
            }
        )
        assert resp.status_code == 201, "Bad HTTP code: " + str(resp.status_code)

    def setPassword(self, username, password):
        userFromDb = User.objects.get(username=username)
        userFromDb.set_password(password)
        userFromDb.save()

    def updateEmail(self, user, email):
        data = {
            "username" : user.username,
            "email"    : email,
            "groups"   : []
        }
        resp = self.client.put(
            path         = reverse('user-detail', args=[user.id]),
            data         = data,
            headers      = { 'Content-Type':'application/json; UTF-8' },
            content_type = "application/json"
        )
        assert resp.status_code == 200, "Bad HTTP code: " + str(resp.status_code)

    def getUser(self, userId):
        resp = self.client.get(reverse('user-detail', args=[userId]))
        assert resp.status_code == 200, "Bad HTTP code: " + str(resp.status_code)
        return json.loads(resp.content)

    def getListLength(self, basename, queryparams=''):
        resp = self.client.get(reverse(basename) + queryparams)
        assert resp.status_code == 200, "Bad HTTP code: " + str(resp.status_code)
        return len(json.loads(resp.content))

    def deleteUser(self, userId):
        return self.client.delete(reverse('user-detail', args=[userId]))

    def createBookmark(self, url, description, isPublic, user):
        resp = self.client.post(
            reverse('bookmark-list'),
            {
                "url"         : url,
                "description" : description,
                "isPublic"    : isPublic,
                "user"        : reverse('user-detail', args=[user.id])
            }
        )
        assert resp.status_code == 201, "Bad HTTP code: " + str(resp.status_code)
