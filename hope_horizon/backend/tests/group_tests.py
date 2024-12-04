from sqlite3 import Date
from rest_framework.test import APITestCase
from rest_framework import status
from freezegun import freeze_time
from backend.models import CustomGroup, GroupUser, UserRole
from backend.models.user import User

class GroupTests(APITestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser1",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        self.user = User.objects.create_user(
            username="testuser2",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        # Create test group
        self.test_group_dict = {
            "name": "testgroup",
            "description": "testdescription",
        }
        
        # Create test group user owner
        self.test_group_user_dict_owner = {
            "user_id": 1,
            "group_id": 1,
            "owner": True,
            "is_active": True,
        }

        # Create test group user not owner
        self.test_group_user_dict_not_owner = {
            "user_id": 2,
            "group_id": 1,
            "owner": False,
            "is_active": True,
        }

        # Login the test users
        self.client.login(username="testuser1", password="testpassword")
        self.client.login(username="testuser2", password="testpassword")

    ###########################################################################################################
    #                                Group "GET(list)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_list_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/group/&owned=True", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #test when owned not given
    def test_group_list_empty_owned(self):
        response = self.client.get("/api/group/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #test when owned is not true
    def test_group_list_owned_false(self):
        response = self.client.post("/api/group/", self.test_group_dict, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/group/&owned=True", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_group(response.data)
    

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_group(self, response_data):
        self.assertGreaterEqual(response_data["id"], 1)
        self.assertEqual(response_data["name"], self.test_group_dict["name"])
        self.assertEqual(response_data["description"], self.test_group_dict["description"])