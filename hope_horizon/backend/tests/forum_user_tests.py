from sqlite3 import Date
from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import Forum, ForumUser, UserRole
from backend.models.user import User

class ForumUserTests(APITestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        self.user4 = User.objects.create_user(
            username="testuser4",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        # Create test forum
        self.test_forum = Forum.objects.create(
            name="testforum",
            description="testdescription"
        )
        self.test_forum_inactive = Forum.objects.create(
            name="testforum2",
            description="testdescription",
            is_active=False
        )
        
        # Create test forum user owner
        self.test_forum_user_owner = ForumUser.objects.create(
            user_id=self.user1,
            forum_id=self.test_forum,
            is_owner=True,
            is_active=True,
        )

        # Create test forum user not owner
        self.test_forum_user_not_owner = ForumUser.objects.create(
            user_id=self.user2,
            forum_id=self.test_forum,
            is_owner=False,
            is_active=True,
        )

        # Login the test users
        self.client.login(username="testuser1", password="testpassword")

    ###########################################################################################################
    #                                Forum "GET(list)" method tests                                     #
    ###########################################################################################################

    # test when a user is not authenticated
    def test_forum_user_list_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/forum-user/", data={"forum_id": "1"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when a user is authenticated but the forum does not exist
    def test_forum_user_list_forum_not_exist(self):
        response = self.client.get("/api/forum-user/", data={"forum_id": "100"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when a user is authenticated but the forum is inactive
    def test_forum_user_list_forum_inactive(self):
        response = self.client.get("/api/forum-user/", data={"forum_id": "2"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when a user is authenticated but the user is not the owner of the forum
    def test_forum_user_list_not_owner(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get("/api/forum-user/", data={"forum_id": self.test_forum.id}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("forum_users", response.data)
        self.assertEqual(len(response.data["forum_users"]), 1)
        self.assertEqual(response.data["forum_users"][0]["user_id"], self.user2.id)
        self.assertFalse(response.data["forum_users"][0]["is_owner"])

    # test that a user can get a list of all forum users
    def test_forum_user_list(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get("/api/forum-user/", data={"forum_id": self.test_forum.id}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("forum_users", response.data)
        self.assertEqual(len(response.data["forum_users"]), 2)  # Both users should be listed


    # test that a user can get a list of all forum users when the user is the owner
    def test_forum_user_list_user_not_member(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.get("/api/forum-user/", data={"forum_id": "1"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    ###########################################################################################################
    #                                Forum "POST(create)" method tests                                     #
    ###########################################################################################################

    # test when everything is correct
    def test_forum_user_create(self):
        response = self.client.post("/api/forum-user/", data={"forum_id": self.test_forum.id, "users": [self.user4.id]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    # test when forum does not exist
    def test_forum_user_create_forum_not_found(self):
        response = self.client.post("/api/forum-user/", data={"forum_id": "999", "users": [self.user3.id]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when forum is not active
    def test_forum_user_create_forum_not_active(self):
        self.test_forum.is_active = False
        self.test_forum.save()
        response = self.client.post("/api/forum-user/", data={"forum_id": "1", "users": [self.user3.id]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when user is not authorized to add forum users
    def test_forum_user_create_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.post("/api/forum-user/", data={"forum_id": "1", "users": [self.user3.id]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test when no users provided
    def test_forum_user_create_no_users_provided(self):
        response = self.client.post("/api/forum-user/", data={"forum_id": "1", "users": []}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when user does not exist
    def test_forum_user_create_user_not_found(self):
        response = self.client.post("/api/forum-user/", data={"forum_id": "1", "users": [10]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when user is not active
    def test_forum_user_create_user_not_active(self):
        self.user3.is_active = False
        self.user3.save()
        response = self.client.post("/api/forum-user/", data={"forum_id": "1", "users": [self.user3.id]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when user already exists in the forum
    def test_forum_user_create_user_already_exists(self):
        response = self.client.post("/api/forum-user/", data={"forum_id": "1", "users": [self.user2.id]}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    ###########################################################################################################
    #                                Forum "DELETE(destroy)" method tests                                     #
    ###########################################################################################################

    # test when everything is correct
    def test_forum_user_destroy(self):
        response = self.client.delete(f"/api/forum-user/{self.test_forum_user_not_owner.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ForumUser.objects.get(pk=self.test_forum_user_not_owner.id).is_active)

    # test when not authenticated
    def test_forum_user_destroy_not_authenticated(self):
        self.client.logout()
        response = self.client.delete(f"/api/forum-user/{self.test_forum_user_not_owner.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when the forum user does not exist
    def test_forum_user_destroy_not_exist(self):
        response = self.client.delete(f"/api/forum-user/10/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when the user is not the owner of the forum
    def test_forum_user_destroy_not_owner(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(f"/api/forum-user/{self.test_forum_user_not_owner.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_forum_user_list(self, response, forum_user_list):
        response_forum_users = response.data["forum_users"]
        self.assertEqual(len(response_forum_users), len(forum_user_list))
        
        for response_forum_user, forum_user in zip(response_forum_users, forum_user_list):
            self.assertEqual(response_forum_user["id"], forum_user.id)
            self.assertEqual(response_forum_user["user_id"], forum_user.user_id.id)
            self.assertEqual(response_forum_user["username"], forum_user.user_id.username)