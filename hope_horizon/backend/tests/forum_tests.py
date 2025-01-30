from sqlite3 import Date
from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import Forum, ForumUser, UserRole
from backend.models.user import User

class ForumTests(APITestCase):

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
    #                                Forum "GET(list)" method tests                                           #
    ###########################################################################################################

    # test if user is not authenticated
    def test_forum_list_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/forum/", data={"owned": "True"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when owned not given
    def test_forum_list_empty_owned(self):
        response = self.client.get("/api/forum/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when owned is true
    def test_forum_list_owned_True(self):
        self.client.logout()
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get("/api/forum/", data={"owned": "True"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_forums(response.data["custom_forums"])

    # test when owned is false
    def test_forum_list_owned_False(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get("/api/forum/", data={"owned": "False"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_forums(response.data["custom_forums"])

    ###########################################################################################################
    #                                Forum "GET(retrieve)" method tests                                       #
    ###########################################################################################################

    # test if user is not authenticated
    def test_forum_retrieve_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/forum/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when forum does not exist
    def test_forum_retrieve_forum_not_exist(self):
        response = self.client.get("/api/forum/10/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when forum is inactive
    def test_forum_retrieve_forum_inactive(self):
        response = self.client.get("/api/forum/2/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when user is not authorized
    def test_forum_retrieve_user_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.get("/api/forum/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test when user is authorized
    def test_forum_retrieve_user_authorized(self):
        response = self.client.get("/api/forum/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_forum(response.data)

    ###########################################################################################################
    #                                Group "POST(create)" method tests                                        #
    ###########################################################################################################

    # test if user is not authenticated
    def test_forum_create_not_authenticated(self):
        self.client.logout()
        response = self.client.post("/api/forum/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when name is not given
    def test_forum_create_no_name(self):
        response = self.client.post("/api/forum/", {"description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # test when description is not given
    def test_forum_create_no_description(self):
        response = self.client.post("/api/forum/", {"name": "testforum3"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # test when forum name already exists
    def test_forum_create_forum_name_exists(self):
        response = self.client.post("/api/forum/", {"name": "testforum", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when serializer is not valid
    def test_forum_create_invalid_data(self):
        response = self.client.post("/api/forum/", {"name": ""}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    # test when everything is correct
    def test_forum_create_success(self):
        response = self.client.post("/api/forum/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._validate_forum(response.data, expected_name="testforum3", expected_description="testdescription")

    ###########################################################################################################
    #                                Group "PUT(update)" method tests                                         #
    ###########################################################################################################

    # test if user is not authenticated
    def test_forum_update_not_authenticated(self):
        self.client.logout()
        response = self.client.put("/api/forum/1/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forum_update_no_name(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.put(f"/api/forum/{self.test_forum.id}/", {"description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # test when description is not given
    def test_forum_update_no_description(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.put(f"/api/forum/{self.test_forum.id}/", {"name": "testforum3"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # test when forum does not exist
    def test_forum_update_forum_not_exist(self):
        response = self.client.put("/api/forum/10/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when forum is inactive
    def test_forum_update_forum_inactive(self):
        response = self.client.put("/api/forum/2/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when user is not authorized
    def test_forum_update_user_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.put("/api/forum/1/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # test when user is authorized
    def test_forum_update_user_authorized(self):
        response = self.client.put(f"/api/forum/1/", {"name": "testforum3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_forum(response.data, expected_name="testforum3", expected_description="testdescription")

    ###########################################################################################################
    #                                Group "DELETE(destroy)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_forum_delete_not_authenticated(self):
        self.client.logout()
        response = self.client.delete("/api/forum/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when forum does not exist
    def test_forum_delete_forum_not_exist(self):
        response = self.client.delete("/api/forum/10/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when forum is inactive
    def test_forum_delete_forum_inactive(self):
        response = self.client.delete("/api/forum/2/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when user is not authorized
    def test_forum_delete_user_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.delete("/api/forum/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test when user is authorized
    def test_forum_delete_user_authorized(self):
        response = self.client.delete("/api/forum/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_forum(self, response, expected_name=None, expected_description=None):
        self.assertGreaterEqual(response["id"], 1)
        if expected_name:
            self.assertEqual(response["name"], expected_name)
        else:
            self.assertEqual(response["name"], self.test_forum.name)
        if expected_description:
            self.assertEqual(response["description"], expected_description)
        else:
            self.assertEqual(response["description"], self.test_forum.description)

    def _validate_forums(self, forums, expected_name=None, expected_description=None):
        for forum in forums:
            self._validate_forum(forum, expected_name, expected_description)