from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import User, BlogPostType
from sqlite3 import Date


class BlogPostTests(APITestCase):
    '''
        Setup and authentication for tests
    '''
    # Setup for tests
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", birthdate=Date(1990, 1, 1)
        )

        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword", birthdate=Date(1990, 1, 1)
        )

        self.blog_post_json = {
            "title": "Test Blog Post",
            "content": "This is a test blog post",
            "blog_post_type_id": 1
        }

        self.client.login(username="testuser", password="testpassword")

    '''
        Test cases for blog post "POST" method
    '''
    # Test if user is not authenticated
    def test_create_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is created
    def test_create_blog_post(self):
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Test Blog Post")
        self.assertEqual(response.data["content"], "This is a test blog post")
        self.assertEqual(response.data["blog_post_type_id"], 1)
        self.assertEqual(response.data["date"], Date.today().strftime("%Y-%m-%d"))
        self.assertGreaterEqual(response.data["id"], 1)

    # Test if blog post title is invalid
    def test_create_blog_post_invalid_title(self):
        self.blog_post_json["title"] = ""
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post content is invalid
    def test_create_blog_post_invalid_content(self):
        self.blog_post_json["content"] = ""
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post type ID is invalid
    def test_create_blog_post_invalid_blog_post_type_id(self):
        self.blog_post_json["blog_post_type_id"] = -1
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    '''
        Test cases for blog post "GET" (by Id) method
    '''   
    # Test if user is not authenticated
    def test_get_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/blog_post/1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is retrieved by owner 
    def test_get_blog_post_allowed_by_owner(self):
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        response = self.client.get(f"/api/blog_post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Blog Post")
        self.assertEqual(response.data["content"], "This is a test blog post")
        self.assertEqual(response.data["blog_post_type_id"], 1)
        self.assertEqual(response.data["date"], Date.today().strftime("%Y-%m-%d"))
        self.assertEqual(response.data["id"], blog_post_id)

    # Test if user is allowed to view blog post of type "Public" (not owned by user)
    def test_get_blog_post_allowed_by_type(self):
        self.blog_post_json["blog_post_type_id"] = BlogPostType.objects.get(type="Public").id
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog_post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test if user is allowed to view blog post by group
    def test_get_blog_post_allowed_by_group(self):
        pass
        # TODO: Implement this test case

    # Test if blog post does not exist
    def test_get_blog_post_does_not_exist(self):
        response = self.client.get("/api/blog_post/-1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # Test if user is not allowed to view blog post of type "Private"
    def test_get_blog_post_not_allowed_by_type_private(self):
        self.blog_post_json["blog_post_type_id"] = BlogPostType.objects.get(type="Private").id
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog_post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test if user is not allowed to view blog post of type "Protected"
    def test_get_blog_post_not_allowed_by_type_protected(self):
        self.blog_post_json["blog_post_type_id"] = BlogPostType.objects.get(type="Protected").id
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog_post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test if user is not allowed to view blog post by group
    def test_get_blog_post_not_allowed_by_group(self):
        pass
        # TODO: Implement this test case
    
    '''
        Test cases for blog post "PUT" method
    '''


    '''
        Test cases for blog post "DELETE" method
    '''
    # Test if user is not authenticated
    def test_delete_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.delete("/api/blog_post/1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is deleted
    def test_delete_blog_post(self):
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        response = self.client.delete(f"/api/blog_post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # Test deleting a blog post that does not exist
    def test_delete_blog_post_does_not_exist(self):
        response = self.client.delete("/api/blog_post/-1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test deleting a blog post that does not belong to the user
    def test_delete_blog_post_not_owned(self):
        response = self.client.post("/api/blog_post/", self.blog_post_json, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(f"/api/blog_post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    '''
        Test cases for blog post "GET" (list) method
    '''
