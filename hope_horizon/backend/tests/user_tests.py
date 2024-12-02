from sqlite3 import Date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from backend.models import UserStatus, User, UserRole
from freezegun import freeze_time
import datetime as dt


class UserTests(APITestCase):

    def setUp(self):
        self.test_user_dict = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@gmail.com",
            "birthdate": Date(1990, 1, 1).strftime("%Y-%m-%d"),
            "user_role_id": UserRole.objects.get(role="User").id,
        }

    ###########################################################################################################
    #                                     User "POST" method tests                                            #
    ###########################################################################################################

    # test user creation with invalid data, invalid username
    def test_create_user_invalid_username(self):
        self.test_user_dict['username'] = ""
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user creation with invalid data, invalid password
    def test_create_user_invalid_password(self):
        self.test_user_dict['password'] = ""    
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user creation with invalid data, invalid email
    def test_create_user_invalid_email(self):
        self.test_user_dict['email'] = "" 
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user creation with invalid data, invalid birthdate
    def test_create_user_invalid_birthdate(self):
        self.test_user_dict['birthdate'] = "" 
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user creation with invalid data, invalid user_role_id
    def test_create_user_invalid_user_role_id(self):
        self.test_user_dict['user_role_id'] = 9999 # invalid user_role_id
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user creation with valid data, user already exists
    def test_create_user_user_exists(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user creation with valid data, user does not exist
    def test_create_user(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._validate_user(response.data)

    ###########################################################################################################
    #                                      User "PUT" method tests                                            #
    ###########################################################################################################

    # test user update not authenticated
    def test_update_user_not_authenticated(self):
        response = self.client.put("/api/user/1/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test user update with invalid data, invalid username
    def test_update_user_invalid_username(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        self.test_user_dict['username'] = ""
        response = self.client.put(f"/api/user/{response["id"]}", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_user(self, response_data):
        self.assertGreaterEqual(response_data["id"], 1)
        self.assertEqual(response_data["username"], self.test_user_dict["username"])
        self.assertEqual(response_data["email"], self.test_user_dict["email"])
        self.assertEqual(response_data["birthdate"], self.test_user_dict["birthdate"])
        self.assertEqual(response_data["user_role_id"], self.test_user_dict["user_role_id"])
