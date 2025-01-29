from sqlite3 import Date
from rest_framework import status
from rest_framework.test import APITestCase

from backend import models


class QuoteTests(APITestCase):

    def setUp(self):
        self.test_user_dict = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@gmail.com",
            "birthdate": Date(1990, 1, 1).strftime("%Y-%m-%d"),
        }

        models.Quote.objects.create(
            quote="test quote",
            author="test author",
        )

        models.Quote.objects.create(
            quote="test quote",
            author="test author",
        )

    ###########################################################################################################
    #                                  User "GET" (list) method tests                                         #
    ###########################################################################################################

    # test user list retrieval not authenticated
    def test_get_quote_list_not_authenticated(self):
        response = self.client.get("/api/quote/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test user list retrieval authenticated
    def test_get_quote_list_authenticated(self):
        response = self.client.post("/api/user/", self.test_user_dict, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.login(username=self.test_user_dict["username"], password=self.test_user_dict["password"])
        response = self.client.get("/api/quote/", format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)