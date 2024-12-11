from sqlite3 import Date
from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import CustomGroup, GroupUser, UserRole
from backend.models.user import User

class GroupTests(APITestCase):

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

        # Create test group
        self.test_group = CustomGroup.objects.create(
            name="testgroup",
            description="testdescription"
        )
        self.test_group_inactive = CustomGroup.objects.create(
            name="testgroup2",
            description="testdescription",
            is_active=False
        )
        
        # Create test group user owner
        self.test_group_user_owner = GroupUser.objects.create(
            user_id=self.user1,
            group_id=self.test_group,
            is_owner=True,
            is_active=True,
        )

        # Create test group user not owner
        self.test_group_user_not_owner = GroupUser.objects.create(
            user_id=self.user2,
            group_id=self.test_group,
            is_owner=False,
            is_active=True,
        )

        # Login the test users
        self.client.login(username="testuser1", password="testpassword")

    ###########################################################################################################
    #                                Group "GET(list)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_list_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/group/", data={"owned": "True"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when owned not given
    def test_group_list_empty_owned(self):
        response = self.client.get("/api/group/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when owned is true
    def test_group_list_owned_True(self):
        self.client.logout()
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get("/api/group/", data={"owned": "True"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_groups(response.data["custom_groups"])

    # test when owned is false
    def test_group_list_owned_False(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get("/api/group/", data={"owned": "False"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_groups(response.data["custom_groups"])

    ###########################################################################################################
    #                                Group "GET(retrieve)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_retrieve_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/group/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when group does not exist
    def test_group_retrieve_group_not_exist(self):
        response = self.client.get("/api/group/10/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when group is inactive
    def test_group_retrieve_group_inactive(self):
        response = self.client.get("/api/group/2/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when user is not authorized
    def test_group_retrieve_user_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.get("/api/group/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test when user is authorized
    def test_group_retrieve_user_authorized(self):
        response = self.client.get("/api/group/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_group(response.data)

    ###########################################################################################################
    #                                Group "POST(create)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_create_not_authenticated(self):
        self.client.logout()
        response = self.client.post("/api/group/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when name is not given
    def test_group_create_no_name(self):
        response = self.client.post("/api/group/", {"description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # test when description is not given
    def test_group_create_no_description(self):
        response = self.client.post("/api/group/", {"name": "testgroup3"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # test when group name already exists
    def test_group_create_group_name_exists(self):
        response = self.client.post("/api/group/", {"name": "testgroup", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when serializer is not valid
    def test_group_create_invalid_data(self):
        response = self.client.post("/api/group/", {"name": ""}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    # test when everything is correct
    def test_group_create_success(self):
        response = self.client.post("/api/group/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._validate_group(response.data, expected_name="testgroup3", expected_description="testdescription")

    ###########################################################################################################
    #                                Group "PUT(update)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_update_not_authenticated(self):
        self.client.logout()
        response = self.client.put("/api/group/1/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when name is not given
    def test_group_update_no_name(self):
        response = self.client.put("/api/group/1/", {"description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # test when description is not given
    def test_group_update_no_description(self):
        response = self.client.put("/api/group/1/", {"name": "testgroup3"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test when group does not exist
    def test_group_update_group_not_exist(self):
        response = self.client.put("/api/group/10/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when group is inactive
    def test_group_update_group_inactive(self):
        response = self.client.put("/api/group/2/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when user is not authorized
    def test_group_update_user_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.put("/api/group/1/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # test when user is authorized
    def test_group_update_user_authorized(self):
        response = self.client.put(f"/api/group/1/", {"name": "testgroup3", "description": "testdescription"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_group(response.data, expected_name="testgroup3", expected_description="testdescription")

    ###########################################################################################################
    #                                Group "DELETE(destroy)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_delete_not_authenticated(self):
        self.client.logout()
        response = self.client.delete("/api/group/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when group does not exist
    def test_group_delete_group_not_exist(self):
        response = self.client.delete("/api/group/10/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when group is inactive
    def test_group_delete_group_inactive(self):
        response = self.client.delete("/api/group/2/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when user is not authorized
    def test_group_delete_user_not_authorized(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.delete("/api/group/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test when user is authorized
    def test_group_delete_user_authorized(self):
        response = self.client.delete("/api/group/1/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_group(self, response, expected_name=None, expected_description=None):
        self.assertGreaterEqual(response["id"], 1)
        if expected_name:
            self.assertEqual(response["name"], expected_name)
        else:
            self.assertEqual(response["name"], self.test_group.name)
        if expected_description:
            self.assertEqual(response["description"], expected_description)
        else:
            self.assertEqual(response["description"], self.test_group.description)

    def _validate_groups(self, groups, expected_name=None, expected_description=None):
        for group in groups:
            self._validate_group(group, expected_name, expected_description)