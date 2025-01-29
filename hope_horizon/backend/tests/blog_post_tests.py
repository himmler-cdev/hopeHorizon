from rest_framework.test import APITestCase
from rest_framework import status
from backend.models import User, BlogPostType, UserRole, Forum, ForumUser
from sqlite3 import Date


class BlogPostTests(APITestCase):
    ###########################################################################################################
    #                                              Setup                                                      #
    ###########################################################################################################

    # Setup for tests
    def setUp(self):
        # Create a test users
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

        self.userTherapist = User.objects.create_user(
            username="testtherapist",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="Therapist"),
        )

        self.userModerator = User.objects.create_user(
            username="testmoderator",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="Moderator"),
        )

        # Create blog post type
        self.blog_post_obj = {
            "title": "Test Blog Post",
            "content": "This is a test blog post",
            "blog_post_type_id": 1
        }

        # Create forum
        self.test_forum = Forum.objects.create(
            name="Test Forum",
            description="This is a test forum"
        )

        # Create forum user
        self.forum_user = ForumUser.objects.create(
            forum_id=self.test_forum,
            user_id=self.user
        )

        self.forum_user2 = ForumUser.objects.create(
            forum_id=self.test_forum,
            user_id=self.user2
        )

        # Login user
        self.client.login(username="testuser", password="testpassword")

    ###########################################################################################################
    #                                     Blog post "POST" method tests                                       #
    ###########################################################################################################

    # Test if user is not authenticated
    def test_create_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is created
    def test_create_blog_post(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._validate_data(response.data)   

    # Test if blog post title is invalid
    def test_create_blog_post_invalid_title(self):
        self.blog_post_obj["title"] = ""
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post content is invalid
    def test_create_blog_post_invalid_content(self):
        self.blog_post_obj["content"] = ""
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post type ID is invalid
    def test_create_blog_post_invalid_blog_post_type_id(self):
        self.blog_post_obj["blog_post_type_id"] = -1
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post type is "Forum" and forum ID is invalid
    def test_create_blog_post_invalid_forum_id(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = -1
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ###########################################################################################################
    #                                     Blog post "GET" (by Id) method tests                                #
    ###########################################################################################################

    # Test if user is not authenticated
    def test_get_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/blog-post/1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is retrieved by owner 
    def test_get_blog_post_allowed_by_owner(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_data(response.data)   

    # Test if user is allowed to view blog post of type "Public" (not owned by user)
    def test_get_blog_post_allowed_by_type(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Public").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test if user is allowed to view blog post by forum
    def test_get_blog_post_allowed_by_forum(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test if blog post does not exist
    def test_get_blog_post_does_not_exist(self):
        response = self.client.get("/api/blog-post/-1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # Test if user is not allowed to view blog post of type "Private"
    def test_get_blog_post_not_allowed_by_type_private(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Private").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test if user is not allowed to view blog post of type "Protected"
    def test_get_blog_post_not_allowed_by_type_protected(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Protected").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test if therapist is allowed to view blog post of type "Protected"
    def test_get_blog_post_allowed_by_type_protected(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Protected").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testtherapist", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    ###########################################################################################################
    #                                     Blog post "PUT" method tests                                        #
    ###########################################################################################################^

    # Test if user is not authenticated
    def test_update_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.put("/api/blog-post/1/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is updated
    def test_update_blog_post(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["title"] = "Updated Blog Post"
        self.blog_post_obj["content"] = "This is an updated blog post"
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._validate_data(response.data)    

    # Test if blog post title is invalid
    def test_update_blog_post_invalid_title(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["title"] = ""
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post content is invalid
    def test_update_blog_post_invalid_content(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["content"] = ""
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Test if blog post type ID is invalid
    def test_update_blog_post_invalid_blog_post_type_id(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["blog_post_type_id"] = -1
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Test if blog post does not exist
    def test_update_blog_post_does_not_exist(self):
        response = self.client.put("/api/blog-post/-1/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test if user has no permission to update blog post
    def test_update_blog_post_not_owned(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    

    # Test if blog post changes blog post type from "Public" to "Forum" and second user can view it
    def test_update_blog_post_change_type_to_forum(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Public").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test if blog post changes blog post type from "Forum" to "Private" and second user can't view it
    def test_update_blog_post_change_type_to_private(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Private").id
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test if blog post type is "Forum" and forum ID is invalid
    def test_update_blog_post_invalid_forum_id(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.blog_post_obj["forum_id"] = -1
        response = self.client.put(f"/api/blog-post/{blog_post_id}/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
     

    ###########################################################################################################
    #                                     Blog post "DELETE" method tests                                     #
    ###########################################################################################################

    # Test if user is not authenticated
    def test_delete_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.delete("/api/blog-post/1/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test if blog post is deleted
    def test_delete_blog_post(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        response = self.client.delete(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    # Test deleting a blog post that does not exist
    def test_delete_blog_post_does_not_exist(self):
        response = self.client.delete("/api/blog-post/9999/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test deleting a blog post that does not belong to the user
    def test_delete_blog_post_not_owned(self):
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.delete(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test deleting a blog post by a moderator
    def test_delete_blog_post_moderator(self):
        self.client.logout()
        self.client.login(username="testmoderator", password="testpassword")

        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        blog_post_id = response.data["id"]

        response = self.client.delete(f"/api/blog-post/{blog_post_id}/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    ###########################################################################################################
    #                                     Blog post "GET" (list) method tests                                 #
    ###########################################################################################################

    # Test if user is not authenticated
    def test_list_blog_post_not_authenticated(self):
        self.client.logout()
        response = self.client.get("/api/blog-post?owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Test if blog post list is retrieved
    def test_list_blog_post(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), response.data["page_information"]["page_size"])
        self._validate_data_list_pagination(response.data)

    ### Pagination Tests ###     
    
    # Test if blog post list is retrieved with pagination
    def test_list_blog_post_pagination(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?page=2&page_size=10&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 10)
        self._validate_data_list_pagination(response.data, 2)

    # Test if blog post list is retrieved with pagination (last page)
    def test_list_blog_post_pagination_last_page(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?page=3&page_size=10&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 2)
        self._validate_data_list_pagination(response.data, 3)

    # Test if blog post list is retrieved with pagination (page size greater than total posts)
    def test_list_blog_post_pagination_page_size_greater_than_total_posts(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?page=1&page_size=100&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 22)
        self._validate_data_list_pagination(response.data, 1, 100)

    # Test if blog post list is retrived with page number greater than total pages
    def test_list_blog_post_pagination_page_number_greater_than_total_pages(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?page=40&page_size=10&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 0)
    
    # Test if blog post list is retrived with page number smaller than 1
    def test_list_blog_post_pagination_negative_page_number(self):
        response = self.client.get("/api/blog-post?page=-1&page_size=10&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post list is retrived with page size smaller than 1
    def test_list_blog_post_pagination_negative_page_size(self):
        response = self.client.get("/api/blog-post?page=1&page_size=-10&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if page parameter is required
    def test_list_blog_post_pagination_no_page(self):
        response = self.client.get("/api/blog-post?owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if page parameter is a string
    def test_list_blog_post_pagination_page_string(self):
        response = self.client.get("/api/blog-post?page=invalid&page_size=10&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if page size parameter is a string
    def test_list_blog_post_pagination_page_size_string(self):
        response = self.client.get("/api/blog-post?page=1&page_size=invalid&owned=true", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ### Search Tests ###  

    # Test if blog post list is retrieved with search
    def test_list_blog_post_search(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?search=Test Blog Post 19&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)
        self.assertEqual(response.data["blog_posts"][0]["title"], "Test Blog Post 19")

    # Test if blog post list is retrieved with search (no results)
    def test_list_blog_post_search_no_results(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?search=Test Blog Post 100&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 0)

    ### Blog Post Type Tests ###

    # Test if blog post list is retrieved with blog post type
    def test_list_blog_post_blog_post_type(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?blog_post_type_id=2&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 5)
        for item in response.data["blog_posts"]:
            self.assertEqual(item["blog_post_type_id"], 2)
    
    # Test if blog post list is retrieved with blog post type (no results)
    def test_list_blog_post_blog_post_type_no_results(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?blog_post_type_id=3&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 0)

    # Test if blog post error is returned with invalid blog post type
    def test_list_blog_post_blog_post_type_invalid(self):
        response = self.client.get("/api/blog-post?blog_post_type_id=-1&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post type is not a number
    def test_list_blog_post_blog_post_type_string(self):
        response = self.client.get("/api/blog-post?blog_post_type_id=invalid&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    ### Owned Tests ###

    # Test if blog post list is retrieved with owned
    def test_list_blog_post_owned(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 10)

    # Test if blog post list is retrieved with not owned and blog post type "Public"
    def test_list_blog_post_not_owned(self):
        data = []
        self._push_data_list(data)
        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")

        response = self.client.get("/api/blog-post?owned=false&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 10)
        for item in response.data["blog_posts"]:
            self.assertEqual(item["blog_post_type_id"], BlogPostType.objects.get(type="Public").id)

    # Test if blog post list is retrieved with invalid owned
    def test_list_blog_post_owned_invalid(self):
        response = self.client.get("/api/blog-post?owned=invalid&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Test if blog post can be retrieved by not owned and blog post type "Private"
    def test_list_blog_post_not_owned_private(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Private").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get("/api/blog-post?owned=false&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 0)

    # Test without owned parameter
    def test_list_blog_post_no_owned(self):
        response = self.client.get("/api/blog-post?page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ### Workspace/Therapist Tests ###

    # Test if blog post list is retrieved with workspace
    def test_list_blog_post_workspace(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Public").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Protected").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testtherapist", password="testpassword")
        response = self.client.get("/api/blog-post?workspace=true&owned=false&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 2)

    # Test if blog post list is retrieved with invalid workspace
    def test_list_blog_post_workspace_invalid(self):
        response = self.client.get("/api/blog-post?workspace=invalid&owned=false&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test if blog post list is retrieved without workspace (should return all public blog posts)
    def test_list_blog_post_no_workspace(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Public").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Protected").id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testtherapist", password="testpassword")
        response = self.client.get("/api/blog-post?owned=false&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)

    ### Forum Tests ###

    # Test if blog post list is retrieved with forum name
    def test_list_blog_post_forum_name(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(f"/api/blog-post?forum_name={self.test_forum.name}&owned=true&page=1&blog_post_type_id=3", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)
        self.assertEqual(response.data["blog_posts"][0]["forum_id"], self.test_forum.id)

    # Test if second user can view blog post by forum name
    def test_list_blog_post_forum_name_not_owned(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(f"/api/blog-post?forum_name={self.test_forum.name}&owned=false&page=1&blog_post_type_id=3", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)

    # Test if user can view blog post by forum name not authorized
    def test_list_blog_post_forum_name_not_authorized(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testtherapist", password="testpassword")
        response = self.client.get(f"/api/blog-post?forum_name={self.test_forum.name}&owned=true&page=1&blog_post_type_id=3", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
  
    # Test if all forum blog posts are retrieved when no forum name is provided
    def test_list_blog_post_forum_name_no_forum_name(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/blog-post?owned=true&page=1&blog_post_type_id=3", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)

    # Test if all forum blog posts are retrieved when forum name is provides but not owned
    def test_list_blog_post_forum_name_no_forum_name_not_owned(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get("/api/blog-post?owned=false&page=1&blog_post_type_id=3", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)

    # Test if no blog psot is retrieved when not in any forum
    def test_list_blog_post_forum_name_no_forum(self):
        self.blog_post_obj["blog_post_type_id"] = BlogPostType.objects.get(type="Forum").id
        self.blog_post_obj["forum_id"] = self.test_forum.id
        response = self.client.post("/api/blog-post/", self.blog_post_obj, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
        self.client.login(username="testtherapist", password="testpassword")
        response = self.client.get("/api/blog-post?owned=true&page=1&blog_post_type_id=3", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 0)

    ### Combined Tests ###

    # Test if blog post list is retrieved with search and blog post type
    def test_list_blog_post_search_blog_post_type(self):
        data = []
        self._push_data_list(data)
        response = self.client.get("/api/blog-post?search=Test Blog Post 19&blog_post_type_id=1&owned=true&page=1", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["blog_posts"]), 1)
        self.assertEqual(response.data["blog_posts"][0]["title"], "Test Blog Post 19")
        self.assertEqual(response.data["blog_posts"][0]["blog_post_type_id"], 1)    

    ###########################################################################################################
    #                                               Helper Function                                           #
    ###########################################################################################################

    ### Validation Functions ### 

    def _validate_data(self, data):
        self.assertEqual(data["title"], self.blog_post_obj["title"])
        self.assertEqual(data["content"], self.blog_post_obj["content"])
        self.assertEqual(data["blog_post_type_id"], self.blog_post_obj["blog_post_type_id"])
        self.assertEqual(data["date"], Date.today().strftime("%Y-%m-%d"))
        self.assertGreaterEqual(data["id"], 1)

    def _validate_data_list_pagination(self, data, page=1, page_size=10):
        # Validate page information
        self.assertEqual(data["page_information"]["page"], page)
        self.assertEqual(data["page_information"]["page_size"], page_size)

        # Validate blog posts
        start_index = (page - 1) * page_size
        for i, item in enumerate(data["blog_posts"]):
            self.assertEqual(item["title"], f"Test Blog Post {i + start_index}")
            self.assertEqual(item["content"], f"This is test blog post {i + start_index}")
            self.assertEqual(item["date"], Date.today().strftime("%Y-%m-%d"))
            self.assertGreaterEqual(item["id"], 1)
            if i + start_index < 5:
                self.assertEqual(item["blog_post_type_id"], 4)
            elif i + start_index < 10:
                self.assertEqual(item["blog_post_type_id"], 2)
            else:
                self.assertEqual(item["blog_post_type_id"], 1)

    ### Sample Data Functions ###
        
    # Helper function to push data to the list for list tests
    def _push_data_list(self, data):
        for i in range(22):
            blog_post_obj = {
                "title": f"Test Blog Post {i}",
                "content": f"This is test blog post {i}",
                "blog_post_type_id": 1
            }
            if i < 5:
                blog_post_obj["blog_post_type_id"] = 4
            elif i < 10:
                blog_post_obj["blog_post_type_id"] = 2

            response = self.client.post("/api/blog-post/", blog_post_obj, format="json", follow=True)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data.append(response.data)
