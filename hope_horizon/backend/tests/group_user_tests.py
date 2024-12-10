from sqlite3 import Date
from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import CustomGroup, GroupUser, UserRole
from backend.models.user import User

class GroupUserTests(APITestCase):

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

    # test when a user is not authenticated
    def test_group_user_list_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/group_user/", data={"group_id": "1"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test when a user is authenticated but the group does not exist
    def test_group_user_list_group_not_exist(self):
        response = self.client.get("/api/group_user/", data={"group_id": "100"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # test when a user is authenticated but the group is inactive
    def test_group_user_list_group_inactive(self):
        response = self.client.get("/api/group_user/", data={"group_id": "2"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test when a user is authenticated but the user is not the owner of the group
    def test_group_user_list_not_owner(self):
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get("/api/group_user/", data={"group_id": "1"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test that a user can get a list of all group users
    def test_group_user_list(self):
        response = self.client.get("/api/group_user/", data={"group_id": "1"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_group_user_list(response, [self.test_group_user_not_owner])

    # test that a user can get a list of all group users when the user is the owner
    def test_group_user_list_user_not_member(self):
        self.client.logout()
        self.client.login(username="testuser3", password="testpassword")
        response = self.client.get("/api/group_user/", data={"group_id": "1"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    ###########################################################################################################
    #                                Group "POST(create)" method tests                                     #
    ###########################################################################################################

    def test_group_user_create(self):
        #TODO: Notifications
        pass

    ###########################################################################################################
    #                                Group "DELETE(destroy)" method tests                                     #
    ###########################################################################################################

    def test_group_user_destroy(self):
        response = self.client.delete(f"/api/group_user/{self.test_group_user_not_owner.id}/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GroupUser.objects.get(pk=self.test_group_user_not_owner.id).is_active)
    

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_group_user_list(self, response, group_user_list):
        response_group_users = response.data["group_users"]
        self.assertEqual(len(response_group_users), len(group_user_list))
        
        for response_group_user, group_user in zip(response_group_users, group_user_list):
            self.assertEqual(response_group_user["id"], group_user.id)
            self.assertEqual(response_group_user["user_id"], group_user.user_id.id)
            self.assertEqual(response_group_user["username"], group_user.user_id.username)