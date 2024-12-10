from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import Notification, User
from datetime import date


class NotificationTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com", birthdate=date(1997, 10, 7)
        )
        self.client.login(username="testuser", password="testpassword")

        # Create some notifications for testing
        self.notification_1 = Notification.objects.create(user=self.user, is_read=False)
        self.notification_2 = Notification.objects.create(user=self.user, is_read=True)

    def test_list_notifications(self):
        # Test if unauthenticated user cannot access notifications
        self.client.logout()
        response = self.client.get(reverse("notification-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test listing notifications when authenticated
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("notification-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response has the correct structure
        self.assertIn("notifications", response.data)
        self.assertEqual(len(response.data["notifications"]), 2)  # Verify 2 notifications returned

    def test_filter_notifications(self):
        # Test filtering notifications by `is_read=False`
        response = self.client.get(reverse("notification-list") + "?is_read=False")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 unread notification

        # Test filtering notifications by `is_read=True`
        response = self.client.get(reverse("notification-list") + "?is_read=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 read notification


    def test_create_notification(self):
        # Test unauthenticated user cannot create notifications
        self.client.logout()
        response = self.client.post(reverse("notification-list"), {"content": "New Notification", "is_read": False})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test creating a notification when authenticated
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
        reverse("notification-list"), {"content": "New Notification", "is_read": False, "user": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the notification was created in the database
        self.assertEqual(Notification.objects.count(), 3)

    def test_update_notification(self):
        # Test updating a notification's `is_read` status
        payload = {"is_read": True}
        response = self.client.patch(
            reverse("notification-detail", args=[self.notification_1.id]), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the notification's `is_read` status was updated
        self.notification_1.refresh_from_db()
        self.assertTrue(self.notification_1.is_read)

    def test_delete_notification(self):
        # Test deleting a notification
        response = self.client.delete(
            reverse("notification-detail", args=[self.notification_1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the notification was deleted
        self.assertEqual(Notification.objects.count(), 1)
