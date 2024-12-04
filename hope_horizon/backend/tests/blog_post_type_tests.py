from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import User, UserRole
from sqlite3 import Date


class BlogPostTypeTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

    # Test if user is not authenticated
    def test_is_not_authenticated(self):
        response = self.client.get("/api/blog_post_type/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if user is authenticated and all types are listed
    def test_list_blog_post_types(self):
        self.client.login(username="testuser", password="testpassword")

        response = self.client.get("/api/blog_post_type/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
