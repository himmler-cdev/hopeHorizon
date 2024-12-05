from sqlite3 import Date
from rest_framework.test import APITestCase
from rest_framework import status
from freezegun import freeze_time
from backend.models import CustomGroup, GroupUser, UserRole
from backend.models.user import User
from backend.serializers.group_serializer import GroupSerializer

class GroupTests(APITestCase):

    def setUp(self):
        # Create test user
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

        # Create test group
        self.test_group = CustomGroup.objects.create(
            name="testgroup",
            description="testdescription"
        )
        
        # Create test group user owner
        self.test_group_user_owner = GroupUser.objects.create(
            user=self.user1,
            group=self.test_group,
            is_owner=True,
            is_active=True,
        )

        # Create test group user not owner
        self.test_group_user_not_owner = GroupUser.objects.create(
            user=self.user2,
            group=self.test_group,
            is_owner=False,
            is_active=True,
        )

        # Login the test users
        self.client.login(username="testuser1", password="testpassword")
        self.client.login(username="testuser2", password="testpassword")

    ###########################################################################################################
    #                                Group "GET(list)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_list_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/group/", data={"owned": "True"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #test when owned not given
    def test_group_list_empty_owned(self):
        response = self.client.get("/api/group/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #test when owned is true
    def test_group_list_owned_True(self):
        self.client.logout()
        self.client.login(username="testuser1", password="testpassword")
        #response = self.client.post("/api/group/", self.test_group2_dict, format="json", follow=True)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/group/", data={"owned": "True"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_groups(response.data["groups"])

    #test when owned is false
    def test_group_list_owned_False(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        #response = self.client.post("/api/group/", self.test_group2_dict, format="json", follow=True)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/group/", data={"owned": "False"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_groups(response.data["groups"])

    ###########################################################################################################
    #                                Group "GET(retrieve)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_group_retrieve_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/group/1", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when group does not exist
    def test_group_retrieve_group_not_exist(self):
        response = self.client.get("/api/group/10", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_groups(self, groups):
        for group in groups:
            self.assertGreaterEqual(group["id"], 1)
            self.assertEqual(group["name"], self.test_group.name)
            self.assertEqual(group["description"], self.test_group.description)


    