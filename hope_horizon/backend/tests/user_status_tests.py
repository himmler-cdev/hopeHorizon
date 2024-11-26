from sqlite3 import Date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import UserStatus, User


class UserStatusTests(APITestCase):

    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", birthdate=Date(1990, 1, 1)
        )
        self.client.login(username="testuser", password="testpassword")

        # Create a UserStatus instance
        self.user_status = UserStatus.objects.create(
            user=self.user,
            date="2024-11-25",
            mood=5,
            energy_level=5,
            sleep_quality=5,
            anxiety_level=5,
            appetite=5,
            content="Feeling good",
        )

    def test_list_user_statuses(self):
        url = reverse("userstatus-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user_status(self):
        url = reverse("userstatus-list")
        data = {
            "user": self.user.id,
            "date": "2024-11-26",
            "mood": 4,
            "energy_level": 4,
            "sleep_quality": 4,
            "anxiety_level": 4,
            "appetite": 4,
            "content": "Feeling okay",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserStatus.objects.count(), 2)
