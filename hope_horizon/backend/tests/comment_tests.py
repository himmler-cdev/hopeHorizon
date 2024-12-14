from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from backend.models import BlogPost
from backend.models import Comment
from backend.models import User
from backend.models.blog_post_type import BlogPostType
from backend.models.user_role import UserRole
from datetime import date

class CommentTests(TestCase):

    ###########################################################################################################
    #                                              Setup                                                      #
    ###########################################################################################################

    def setUp(self):
        # Create test data
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            password="password",
            user_role_id=UserRole.objects.get(role="User"),
            birthdate="2024-12-12"
            )
        
        self.user2 = User.objects.create_user(
            username="otheruser",
            password="password2",
            user_role_id=UserRole.objects.get(role="User"),
            birthdate="2024-12-12"
            )
        
        self.user3 = User.objects.create_user(
            username="moderator",
            password="password3",
            user_role_id=UserRole.objects.get(role="Moderator"),
            birthdate="2024-12-12"
            )
        
        self.user4 = User.objects.create_user(
            username="therapist",
            password="password4",
            user_role_id=UserRole.objects.get(role="Therapist"),
            birthdate="2024-12-12"
            )
        
        self.blog_post = BlogPost.objects.create(
            title="Test Blog",
            content="Test Content",
            user_id=self.user,
            blog_post_type_id=BlogPostType.objects.get(type="Public"))
        
        self.blog_post2 = BlogPost.objects.create(
            title="Private Blog",
            content="Test Content",
            user_id=self.user,
            blog_post_type_id=BlogPostType.objects.get(type="Private"))
        
        self.blog_post3 = BlogPost.objects.create(
            title="Protected Blog",
            content="Test Content",
            user_id=self.user,
            blog_post_type_id=BlogPostType.objects.get(type="Protected"))
            
        self.comment = Comment.objects.create(
            content="Test Comment", 
            blog_post_id=self.blog_post, 
            user_id=self.user
        )

        self.comment2 = Comment.objects.create(
            content="Private Comment",
            blog_post_id=self.blog_post2,
            user_id=self.user
        )

        self.comment3 = Comment.objects.create(
            content="Protected Comment",
            blog_post_id=self.blog_post3,
            user_id=self.user
        )

        # Authenticate test user
        self.client.login(username="testuser", password="password")

    ###########################################################################################################
    #                                Group "GET(retrieve)" method tests                                       #
    ###########################################################################################################

    def test_get_comment_unauthenticated(self):
        # Test posting comment when unauthenticated
        self.client.logout()
        response = self.client.get(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comment_by_id(self):
        # Test retrieving a specific comment by ID
        response = self.client.get(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Test Comment")
        self.assertEqual(response.data["user_id"], 1)

    def test_get_comment_moderator(self):
        # Test if moderator can retrieve other user's comments
        self.client.logout()
        self.client.login(username="moderator", password="password3")
        response = self.client.get(f"/api/comment/{self.comment3.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_moderator_protected(self):
        # Test if moderator can retrieve other user's protected comments
        self.client.logout()
        self.client.login(username="moderator", password="password3")
        response = self.client.get(f"/api/comment/{self.comment3.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_therapist(self):
        # Test if therapist can retrieve other user's comments
        self.client.logout()
        self.client.login(username="therapist", password="password4")
        response = self.client.get(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_therapist_protected(self):
        # Test if therapist can retrieve other user's protected comments
        self.client.logout()
        self.client.login(username="therapist", password="password4")
        response = self.client.get(f"/api/comment/{self.comment3.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_bad_request(self):
        # Test retrieving a comment with an invalid ID
        response = self.client.get("/api/comment/notanumber/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get("/api/comment/!/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_comment_private_blog_post(self):
        # Test retrieving a comment on a private blog post
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        response = self.client.get(f"/api/comment/{self.comment2.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_comment_protected_blog_post(self):
        # Test retrieving a comment on a protected blog post
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        response = self.client.get(f"/api/comment/{self.comment3.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_comment_not_found(self):
        # Test retrieving a non existant comment
        response = self.client.get("/api/comment/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ###########################################################################################################
    #                                Group "GET(list)" method tests                                           #
    ###########################################################################################################

    def test_get_comments_list_unauthenticated(self):
        # Test retrieving comments when unauthenticated
        self.client.logout()
        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_list(self):
        # Test retrieving comments for a specific blog post
        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pageInformation"]["actualSize"], 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], "Test Comment")

    def test_get_comments_list_moderator(self):
        # Test if moderator can retrieve comments for other user's blog post
        self.client.logout()
        self.client.login(username="moderator", password="password3")
        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pageInformation"]["actualSize"], 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], "Test Comment")
    
    def test_get_comments_list_therapist(self):
        # Test if therapist can retrieve comments for other user's blog post
        self.client.logout()
        self.client.login(username="therapist", password="password4")
        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pageInformation"]["actualSize"], 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], "Test Comment")

    def test_get_comments_list_moderator_protected(self):
        # Test if moderator can retrieve comments for other user's protected blog post
        self.client.logout()
        self.client.login(username="moderator", password="password3")
        response = self.client.get(f"/api/comment?blog={self.blog_post3.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pageInformation"]["actualSize"], 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], "Protected Comment")

    def test_get_comments_list_therapist_protected(self):
        # Test if therapist can retrieve comments for other user's protected blog post
        self.client.logout()
        self.client.login(username="therapist", password="password4")
        response = self.client.get(f"/api/comment?blog={self.blog_post3.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pageInformation"]["actualSize"], 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["content"], "Protected Comment")

    def test_get_comments_list_pagination(self):
        # Test pagination when there are more than 10 comments
        for i in range(15):
            Comment.objects.create(
                content=f"Test Comment {i}",
                date=date.today(),
                blog_post_id=self.blog_post,
                user_id=self.user
            )

        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["comments"]), 10)

        response = self.client.get(f"/api/comment?blog={self.blog_post.id}&page=1", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["comments"]), 6)
    
    def test_get_comments_list_bad_request(self):
        # Test retrieving comments without blog post ID
        response = self.client.get("/api/comment?page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test retrieving comments with an invalid blog post ID
        response = self.client.get("/api/comment?blog=notanumber&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_comments_list_private_blog_post(self):
        # Test retrieving comments for a private blog post
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        response = self.client.get(f"/api/comment?blog={self.blog_post2.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_comments_list_protected_blog_post(self):
        # Test retrieving comments for a protected blog post
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        response = self.client.get(f"/api/comment?blog={self.blog_post3.id}&page=0", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_comments_list_not_found(self):
        # Test retrieving comments for a non existant blog post
        response = self.client.get("/api/comment?blog=99999999999999999999999999999&page=1", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ###########################################################################################################
    #                                     Comment "Post" method tests                                         #
    ###########################################################################################################

    def test_create_comment_unauthenticated(self):
        # Test posting comment when unauthenticated
        self.client.logout()
        response = self.client.post(f"/api/comment/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment(self):
        # Test creating a new comment
        data = {
            "blog_post_id": self.blog_post.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "New Comment")
        self.assertEqual(response.data["user_id"], 1)

    def test_create_comment_own_private_blog_post(self):
        # Test creating a comment on own private blog post
        data = {
            "blog_post_id": self.blog_post2.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_own_protected_blog_post(self):
        # Test creating a comment on own protected blog post
        data = {
            "blog_post_id": self.blog_post3.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_protected_blog_post_therapist(self):
        # Test creating a comment on a protected blog post as a therapist
        self.client.logout()
        self.client.login(username="therapist", password="password4")
        data = {
            "blog_post_id": self.blog_post3.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_bad_request_content(self):
        # Test creating a comment without content
        data = {
            "blog_post_id": self.blog_post.id
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_bad_request_blog(self):
        # Test creating a comment without blog post ID
        data = {
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_comment_private_blog_post(self):
        # Test creating a comment on a private blog post
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        data = {
            "blog_post_id": self.blog_post2.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment_protected_blog_post(self):
        # Test creating a comment on a protected blog post
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        data = {
            "blog_post_id": self.blog_post3.id,
            "content": "New Comment"
        }
        response = self.client.post("/api/comment/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #TODO: either 404 or 400 depending on if serializer validation or try block in view set is first, can't have both
    #def test_create_comment_blog_post_not_found(self):
        # Test creating a comment with a non existant blog post ID
    #    data = {
    #        "blog_post_id": -1,
    #        "content": "New Comment"
    #    }
    #   response = self.client.post("/api/comment/", data)
    #    self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    #TODO: add notification creation test

    ###########################################################################################################
    #                                     Comment "PUT" method tests                                          #
    ###########################################################################################################

    def test_update_comment_unauthenticated(self):
        # Test updating comment when unauthenticated
        self.client.logout()
        response = self.client.put(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_comment(self):
        # Test updating an existing comment
        data = {"content": "Updated Comment"}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated Comment")

    def test_update_comment_moderator(self):
        # Test if moderator can update other user's comments
        self.client.logout()
        self.client.login(username="moderator", password="password3")
        data = {"content": "Updated Comment"}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Updated Comment")

    def test_update_comment_bad_request_parameter(self):
        # Test updating a comment with an invalid ID
        data = {"content": "Invalid Update"}
        response = self.client.put("/api/comment/notanumber/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put("/api/comment/!/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment_bad_request_content(self):
        # Test updating a comment without content
        data = {}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_comment_permission_denied(self):
        # Test updating a comment by a different user
        self.client.login(username="otheruser", password="password2")
        data = {"content": "Invalid Update"}
        response = self.client.put(f"/api/comment/{self.comment.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_not_found(self):
        # Test updating non existant comment
        data = {"content": "Invalid Update"}
        response = self.client.put("/api/comment/0/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ###########################################################################################################
    #                                    Comment "DELETE" method tests                                        #
    ###########################################################################################################
    
    def test_delete_comment_unauthenticated(self):
        # Test deleting comment when unauthenticated
        self.client.logout()
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment(self):
        # Test deleting a comment
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())
    
    def test_delete_comment_moderator(self):
        # Test if moderator can delete other user's comments
        self.client.logout()
        self.client.login(username="moderator", password="password3")
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_comment_bad_request(self):
        # Test deleting a comment with an invalid ID
        response = self.client.delete("/api/comment/notanumber/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete("/api/comment/!/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_comment_permission_denied(self):
        # Test deleting a comment by a different user
        self.client.logout()
        self.client.login(username="otheruser", password="password2")
        response = self.client.delete(f"/api/comment/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_not_found(self):
        # Test deleting non existant comment
        response = self.client.delete(f"/api/comment/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
