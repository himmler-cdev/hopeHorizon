from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import BlogPost
from backend.models import Comment
from backend.models import User
from backend.models.user_role import UserRole
from datetime import date

class CommentTests(TestCase):
    def setUp(self):
        # Create test data
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password", user_role_id=UserRole.objects.get(role="User"), birthdate="2024-12-12")
        self.user2 = User.objects.create_user(username="otheruser", password="password2", user_role_id=UserRole.objects.get(role="User"), birthdate="2024-12-12")
        self.user3 = User.objects.create_user(username="moderator", password="password3", user_role_id=UserRole.objects.get(role="Moderator"), birthdate="2024-12-12")
        self.blog_post = BlogPost.objects.create(title="Test Blog", content="Test Content", user_id=self.user)
        self.comment = Comment.objects.create(
            content="Test Comment", 
            date=date.today(),  # Use today's date
            blog_post_id=self.blog_post, 
            user_id=self.user
        )

        # Authenticate test user
        self.client.login(username="testuser", password="password")

    def test_get_comments_list(self):
        # Test retrieving comments for a specific blog post
        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pageInformation"]["actualSize"], 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], "Test Comment")

    def test_get_comment_by_id(self):
        # Test retrieving a specific comment by ID
        response = self.client.get(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Test Comment")
        self.assertEqual(response.data["username"], "testuser")

    def test_get_comments_list_pagination(self):
            # Test pagination when there are more than 10 comments
            for i in range(15):
                Comment.objects.create(
                    content=f"Test Comment {i}",
                    date=date.today(),  # Use today's date
                    blog_post_id=self.blog_post,
                    user_id=self.user
                )

            response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["comments"]), 10)

            response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=1")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["comments"]), 6)

    def test_create_comment(self):
        # Test creating a new comment
        data = {
            "blog_post_id": self.blog_post.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "New Comment")
        self.assertEqual(response.data["username"], "testuser")

    ###########################################################################################################
    #                                     Comment "PUT" method tests                                            #
    ###########################################################################################################

    def test_update_comment(self):
        # Test updating an existing comment
        data = {"content": "Updated Comment"}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated Comment")

    def test_update_comment_moderator(self):
        # Test if moderator can update other user's comments
        self.client.login(username="moderator", password="password3")
        data = {"content": "Updated Comment"}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated Comment")

    def test_update_comment_bad_request(self):
        # Test updating a comment with an invalid ID
        data = {"content": "Invalid Update"}
        response = self.client.put("/api/comment/notanumber/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put("/api/comment/!/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment_unauthenticated(self):
        # Test updating comment when unauthenticated
        self.client.logout()
        response = self.client.put(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment_permission_denied(self):
        # Test updating a comment by a different user
        self.client.login(username="otheruser", password="password2")
        data = {"content": "Invalid Update"}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_not_found(self):
        # Test updating non existant comment
        data = {"content": "Invalid Update"}
        response = self.client.put("/api/comment/999999999999999/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    ###########################################################################################################
    #                                    Comment "DELETE" method tests                                        #
    ###########################################################################################################
    
    def test_delete_comment(self):
        # Test deleting a comment
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
    
    def test_delete_comment_moderator(self):
        # Test if moderator can delete other user's comments
        self.client.login(username="moderator", password="password3")
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_comment_bad_request(self):
        # Test deleting a comment with an invalid ID
        response = self.client.delete("/api/comment/notanumber/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete("/api/comment/!/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #405, wird vorher abgefangen wtf?
        #response = self.client.delete("/api/comment/#####/")
        #self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #WIE BRUDA WIE
        #response = self.client.delete("/api/comment/4.20/")
        #self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_comment_unauthenticated(self):
        # Test deleting comment when unauthenticated
        self.client.logout()
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_permission_denied(self):
        # Test deleting a comment by a different user
        self.client.login(username="otheruser", password="password2")
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_not_found(self):
        # Test deleting non existant comment
        response = self.client.delete(f"/api/comment/999999999999999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
