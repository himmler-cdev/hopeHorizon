from sqlite3 import Date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from backend.models import UserStatus, User
from freezegun import freeze_time
import datetime as dt


class UserStatusTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", birthdate=Date(1990, 1, 1)
        )

    def test_list_user_statuses(self):
        pass

    def test_create_user_status(self):
        # test data
        data = {
            "mood": 4,
            "energy_level": 4,
            "sleep_quality": 4,
            "anxiety_level": 4,
            "appetite": 4,
            "content": "Feeling okay",
        }

        # test if user is not authenticated
        response = self.client.post("/api/user_status/", data, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # test if user is authenticated and data is invalid
        self.client.login(username="testuser", password="testpassword")
        data.pop("mood")
        response = self.client.post("/api/user_status/", data, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data["mood"] = 4

        # test if user is authenticated and data is valid
        response = self.client.post("/api/user_status/", data, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test if user is authenticated and entry already exists
        response = self.client.post("/api/user_status/", data, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test if user is authenticated and test different dates
        today = dt.date(2000, 1, 1)
        for i in range(10):
            freezer = freeze_time(today + dt.timedelta(days=i))
            freezer.start()
            response = self.client.post("/api/user_status/", data, format="json", follow=True)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            freezer.stop()

