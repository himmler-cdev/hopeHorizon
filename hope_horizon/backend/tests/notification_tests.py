from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import *
from datetime import date


class NotificationTests(TestCase):

###########################################################################################################
#                                              Setup                                                      #
###########################################################################################################

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            user_role_id=UserRole.objects.get(role="User"),
            birthdate="2024-12-12"
            )
        
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="password",
            user_role_id=UserRole.objects.get(role="User"),
            birthdate="2024-12-12"
            )
        
        self.blog_post = BlogPost.objects.create(
            title="Test Blog",
            content="Test Content",
            user_id=self.user,
            blog_post_type_id=BlogPostType.objects.get(type="Public"))
        
        self.comment = Comment.objects.create(
            content="Test Comment", 
            blog_post_id=self.blog_post, 
            user_id=self.user
        )

        self.notification = Notification.objects.create(
            is_read=False,
            content=f"A new comment was added to your blog post: {self.blog_post.title}",
            user_id=self.user,
            comment_id=self.comment
        )

        # Authenticate test user
        self.client.login(username="testuser", password="password")

    ###########################################################################################################
    #                                Notification "GET(list)" method tests                                           #
    ###########################################################################################################

    def test_get_notifications_list_unauthenticated(self):
        # Test to verify that unauthenticated users cannot access the notifications list
        self.client.logout()
        response = self.client.get("/api/notification/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_notifications_list(self):
        # Test to verify that authenticated users can access the notifications list
        data = {
        "content": "Test Comment",
        "blog_post_id": self.blog_post.id
        }
        response = self.client.post("/api/comment/", data)

        response = self.client.get("/api/notification/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification = response.data["notifications"][0]
        self.assertEqual(notification["content"], f"A new comment was added to your blog post: {self.blog_post.title}")
        self.assertEqual(notification["user_id"], self.user.id)
        self.assertFalse(notification["is_read"])

    def test_get_notifications_list_forum_invitation(self):
        # Test to verify that a forum invitation creats a notification
        self.client.logout()
        self.client.login(username="testuser2", password="password")
        forum = Forum.objects.create(name="Test Forum", description="Test Description")

        ForumUser.objects.create(user_id=self.user2, forum_id=forum, is_owner=True, is_active=True)
        data = {"forum_id": 1,"users": [self.user.id]}
        response = self.client.post("/api/forum-user/", data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()
        self.client.login(username="testuser", password="password")
        response = self.client.get("/api/notification/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notification = response.data["notifications"][1]
        self.assertEqual(notification["content"], f"You have been invited to forum: {forum.name}")
        self.assertEqual(notification["user_id"], self.user.id)
        self.assertFalse(notification["is_read"])

    ###########################################################################################################
    #                                    Comment "DELETE" method tests                                        #
    ###########################################################################################################

    def test_delete_notification_unauthenticated(self):
        # Test to verify that unauthenticated users cannot delete notifications
        self.client.logout()
        response = self.client.delete("/api/notification/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_notification(self):
        # Test to verify that notifications can be deleted
        response = self.client.delete(f"/api/notification/{self.notification.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)

    def test_delete_notification_invalid_id(self):
        # Test to verify that notifications with invalid ID formats cannot be deleted
        response = self.client.delete("/api/notification/abc/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_notification_permission_denied(self):
        # Test to verify that users can only delete their own notifications
        self.client.logout()
        self.client.login(username="testuser2", password="password")
        response = self.client.delete(f"/api/notification/{self.notification.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_notification_not_found(self):
        # Test to verify that non existant notifications cannot be deleted
        response = self.client.delete("/api/notification/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
