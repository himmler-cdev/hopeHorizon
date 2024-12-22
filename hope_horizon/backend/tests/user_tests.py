from sqlite3 import Date
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import UserRole


class UserTests(APITestCase):

    def setUp(self):
        self.test_user_dict = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@gmail.com",
            "birthdate": Date(1990, 1, 1).strftime("%Y-%m-%d"),
        }

    ###########################################################################################################
    #                                  User "GET" (list) method tests                                         #
    ###########################################################################################################

    # test user list retrieval not authenticated
    def test_get_user_list_not_authenticated(self):
        response = self.client.get("/api/user/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test user list retrieval authenticated
    def test_get_user_list(self):
        usersnames = ["testuser"]
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.get("/api/user/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["users"]), 1)
        self._validate_user_list(usersnames, response.data["users"])

    # test user list retrieval authenticated, search parameter
    def test_get_user_list_search(self):
        usersnames = ["testuser", "testuser2", "testuser3", "testuser4", "hans", "peter"]
        for username in usersnames:
            self.test_user_dict["username"] = username
            self.test_user_dict["email"] = f"{username}@gmail.com"
            response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.get("/api/user/?search=testuser", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["users"]), 4)
        self._validate_user_list(usersnames[:-2], response.data["users"])

    ###########################################################################################################
    #                                     User "GET" method tests                                             #
    ###########################################################################################################

    # test user retrieval not authenticated
    def test_get_user_not_authenticated(self):
        response = self.client.get("/api/user/username/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test user retrieval authenticated, user does not exist
    def test_get_user_does_not_exist(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.get("/api/user/username2/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test user retrieval authenticated, user does not have permission
    def test_get_user_no_permission(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        username = response.data["username"]
        self.test_user_dict["username"] = "testuser2"
        self.test_user_dict["email"] = "test2@gmail.com"
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.get(f"/api/user/{username}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # test user retrieval authenticated, user has permission
    def test_get_user(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.get(f"/api/user/{response.data["username"]}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user(response.data)


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
        response = self.client.put(f"/api/user/{response.data["id"]}/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user update with invalid data, invalid password
    def test_update_user_invalid_password(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        self.test_user_dict['password'] = ""
        response = self.client.put(f"/api/user/{response.data["id"]}/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user update with invalid data, invalid email
    def test_update_user_invalid_email(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        self.test_user_dict['email'] = ""
        response = self.client.put(f"/api/user/{response.data["id"]}/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user update with invalid data, invalid birthdate
    def test_update_user_invalid_birthdate(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        self.test_user_dict['birthdate'] = ""
        response = self.client.put(f"/api/user/{response.data["id"]}/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user update with valid data, user does not exist
    def test_update_user_user_does_not_exist(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.put("/api/user/2/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test user update with valid data, user does not have permission
    def test_update_user_no_permission(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        id = response.data["id"]
        self.test_user_dict["username"] = "testuser2"
        self.test_user_dict["email"] = "test2@gmail.com"
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.put(f"/api/user/{id}/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test user update with invalid data, invalid id
    def test_update_user_invalid_id(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.put("/api/user/thisIsNotANumber/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user update with valid data, user has permission
    def test_update_user(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        self.test_user_dict["username"] = "testuser2"
        self.test_user_dict["email"] = "change@gmail.com"
        self.test_user_dict["password"] = "test"
        response = self.client.put(f"/api/user/{response.data["id"]}/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user(response.data)
        self.client.logout()
        self.assertTrue(self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"]))

    ###########################################################################################################
    #                                     User "DELETE" method tests                                          #
    ###########################################################################################################

    # test user deletion not authenticated
    def test_delete_user_not_authenticated(self):
        response = self.client.delete("/api/user/1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test user deletion, user does not exist
    def test_delete_user_does_not_exist(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.delete("/api/user/2/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test user deletion, user does not have permission
    def test_delete_user_no_permission(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        id = response.data["id"]
        self.test_user_dict["username"] = "testuser2"
        self.test_user_dict["email"] = "test2@gmail.com"
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.delete(f"/api/user/{id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test user deletion with invalid data, invalid id
    def test_delete_user_invalid_id(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.delete(f"/api/user/thisIsNotANumber/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user deletion, user has permission
    def test_delete_user(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.delete(f"/api/user/{response.data["id"]}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"]))

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_user(self, response_data):
        self.assertGreaterEqual(response_data["id"], 1)
        self.assertEqual(response_data["username"], self.test_user_dict["username"])
        self.assertEqual(response_data["email"], self.test_user_dict["email"])
        self.assertEqual(response_data["birthdate"], self.test_user_dict["birthdate"])
        self.assertEqual(response_data["user_role"], "User")

    def _validate_user_list(self, usernames, response_data):
        for i in range(len(response_data)):
            self.assertGreaterEqual(response_data[i]["id"], 1)
            self.assertEqual(response_data[i]["username"], usernames[i])
