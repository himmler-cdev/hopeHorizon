from sqlite3 import Date
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import User, UserRole


class UserTrackerTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
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

        # Create a test user tracker json
        self.test_user_tracker_dict = {
            "is_enabled": True,
            "track_mood": True,
            "track_energy_level": False,
            "track_sleep_quality": True,
            "track_anxiety_level": False,
            "track_appetite": True,
            "track_content": False,
        }

        # Login the test users
        self.client.login(username="testuser", password="testpassword")

    ###########################################################################################################
    #                                UserTracker "GET(list)" method tests                                     #
    ###########################################################################################################

    # test if user is not authenticated
    def test_list_user_tracker_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test if user is authenticated and the logged in user has no user tracker entry
    def test_list_user_tracker_no_entry(self):
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # test if user is authenticated and the logged in user has a user tracker entry
    def test_list_user_tracker__with_entry(self):
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_tracker(response.data)

    ###########################################################################################################
    #                                   UserTracker "POST" method tests                                       #
    ###########################################################################################################

    # test if user is not authenticated
    def test_create_user_tracker_not_authenticated(self):
        self.client.logout()
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test if user is authenticated and the data is invalid, missing is_enabled
    def test_create_user_tracker_invalid_data_is_enabled(self):
        self.test_user_tracker_dict.pop("is_enabled")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the data is invalid, missing track_mood
    def test_create_user_tracker_invalid_data_track_mood(self):
        self.test_user_tracker_dict.pop("track_mood")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the data is invalid, missing track_energy_level
    def test_create_user_tracker_invalid_data_track_energy_level(self):
        self.test_user_tracker_dict.pop("track_energy_level")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the data is invalid, missing track_sleep_quality
    def test_create_user_tracker_invalid_data_track_sleep_quality(self):
        self.test_user_tracker_dict.pop("track_sleep_quality")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the data is invalid, missing track_anxiety_level
    def test_create_user_tracker_invalid_data_track_anxiety_level(self):
        self.test_user_tracker_dict.pop("track_anxiety_level")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the data is invalid, missing track_appetite
    def test_create_user_tracker_invalid_data_track_appetite(self):
        self.test_user_tracker_dict.pop("track_appetite")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the data is invalid, missing track_content
    def test_create_user_tracker_invalid_data_track_content(self):
        self.test_user_tracker_dict.pop("track_content")
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated, data is valid and the user has no user tracker entry
    def test_create_user_tracker_valid_data(self):
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_tracker(response.data)

    # test if user is authenticated, data is valid and the user has already a user tracker entry
    def test_create_user_tracker_valid_data_with_existing_entry(self):
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ###########################################################################################################
    #                                    UserTracker "PUT" method tests                                       #
    ###########################################################################################################

    # test if user is not authenticated
    def test_update_user_tracker_not_authenticated(self):
        self.client.logout()
        response = self.client.put(
            "/api/user_tracker/1/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test if user is authenticated and the data is invalid
    def test_update_user_tracker_invalid_data(self):
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_user_tracker_dict.pop("is_enabled")
        response = self.client.put(
            "/api/user_tracker/1/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test if user is authenticated and the user tracker entry does not exist
    def test_update_user_tracker_not_exist(self):
        response = self.client.put(
            "/api/user_tracker/1/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test if user is authenticated, data is valid but the user tracker entry is not owned by the user
    def test_update_user_tracker_exists_not_owned(self):
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.put(
            "/api/user_tracker/1/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_update_user_tracker_exists_owned(self):
        response = self.client.post(
            "/api/user_tracker/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in self.test_user_tracker_dict.items():
            self.test_user_tracker_dict[key] = not value
        response = self.client.put(
            "/api/user_tracker/1/", data=self.test_user_tracker_dict, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_tracker(response.data)

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_user_tracker(self, response_data):
        self.assertGreaterEqual(response_data["id"], 1)
        self.assertEqual(
            response_data["is_enabled"], self.test_user_tracker_dict["is_enabled"]
        )
        self.assertEqual(
            response_data["track_mood"], self.test_user_tracker_dict["track_mood"]
        )
        self.assertEqual(
            response_data["track_energy_level"],
            self.test_user_tracker_dict["track_energy_level"],
        )
        self.assertEqual(
            response_data["track_sleep_quality"],
            self.test_user_tracker_dict["track_sleep_quality"],
        )
        self.assertEqual(
            response_data["track_anxiety_level"],
            self.test_user_tracker_dict["track_anxiety_level"],
        )
        self.assertEqual(
            response_data["track_appetite"], self.test_user_tracker_dict["track_appetite"]
        )
        self.assertEqual(
            response_data["track_content"], self.test_user_tracker_dict["track_content"]
        )
