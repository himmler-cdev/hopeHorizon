from sqlite3 import Date
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from backend.models import User, UserTracker, UserRole
from freezegun import freeze_time


class UserTrackerTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User")
        )

        # Create a test user tracker json
        self.user_tracker_json = {
            "is_enabled": True,
            "track_mood": True,
            "track_energy_level": False,
            "track_sleep_quality": True,
            "track_anxiety_level": False,
            "track_appetite": True,
            "track_content": False,
        }

    def test_list_user_tracker(self):
        # test if user is not authenticated
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test if user is authenticated and the logged in user has no user tracker entry
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # test if user is authenticated and the logged in user has a user tracker entry
        response = self.client.post("/api/user_tracker/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_tracker(response.data)

    def test_create_user_tracker(self):
        # test if user is not authenticated
        response = self.client.post("/api/user_tracker/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test if user is authenticated and the data is invalid
        self.client.login(username="testuser", password="testpassword")
        self.user_tracker_json.pop("is_enabled")
        response = self.client.post("/api/user_tracker/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user_tracker_json["is_enabled"] = True

        # test if user is authenticated, data is valid and the user has no user tracker entry
        response = self.client.post("/api/user_tracker/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/user_tracker/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_tracker(response.data)

        # test if user is authenticated, data is valid and the user has already a user tracker entry
        response = self.client.post("/api/user_tracker/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_tracker(self):
        # test if user is not authenticated
        response = self.client.put("/api/user_tracker/1/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test if user is authenticated and the data is invalid
        self.client.login(username="testuser", password="testpassword")
        self.user_tracker_json.pop("is_enabled")
        response = self.client.put("/api/user_tracker/1/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user_tracker_json["is_enabled"] = True

        # test if user is authenticated, data is valid and the user has no user tracker entry
        response = self.client.put("/api/user_tracker/1/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test if user is authenticated, data is valid and the user has a user tracker entry
        response = self.client.post("/api/user_tracker/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put("/api/user_tracker/1/", data=self.user_tracker_json, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_user_tracker(response.data)


    def _validate_user_tracker(self, response_data):
        self.assertGreaterEqual(response_data["id"], 1)
        self.assertEqual(response_data["is_enabled"], self.user_tracker_json["is_enabled"])
        self.assertEqual(response_data["track_mood"], self.user_tracker_json["track_mood"])
        self.assertEqual(response_data["track_energy_level"], self.user_tracker_json["track_energy_level"])
        self.assertEqual(response_data["track_sleep_quality"], self.user_tracker_json["track_sleep_quality"])
        self.assertEqual(response_data["track_anxiety_level"], self.user_tracker_json["track_anxiety_level"])
        self.assertEqual(response_data["track_appetite"], self.user_tracker_json["track_appetite"])
        self.assertEqual(response_data["track_content"], self.user_tracker_json["track_content"])
