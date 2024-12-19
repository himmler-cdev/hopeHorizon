from sqlite3 import Date
from rest_framework import status
from rest_framework.test import APITestCase
from backend.models import User, UserRole
from freezegun import freeze_time
import datetime as dt


class UserStatusTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            birthdate=Date(1990, 1, 1),
            user_role_id=UserRole.objects.get(role="User"),
        )

        # Create a test user status json
        self.test_user_status_dict = {
            "mood": 4,
            "energy_level": 4,
            "sleep_quality": 4,
            "anxiety_level": 4,
            "appetite": 4,
            "content": "Feeling okay",
        }

        # Login the test user
        self.client.login(username="testuser", password="testpassword")

    ###########################################################################################################
    #                                  UserStatus "GET(list)" method tests                                    #
    ###########################################################################################################

    # test if user is not authenticated
    def test_list_user_statuses_unauthenticated(self):
        self.client.logout()
        response = self.client.get(
            "/api/user-status/", {"from": "2000-01-01"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # query parameters are invalid
    def test_list_user_statuses_invalid_parameters(self):
        response = self.client.get("/api/user-status/", follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # query parameters from date is invalid
    def test_list_user_statuses_invalid_from_date(self):
        response = self.client.get("/api/user-status/", {"from": "thisIsNotADate"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # query parameters to date is invalid
    def test_list_user_statuses_invalid_to_date(self):
        response = self.client.get("/api/user-status/", {"from": "1990-01-01", "to": "thisIsNotADate"}, follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # query parameters are valid
    def test_list_user_statuses_valid_parameters(self):
        response = self.client.post(
            "/api/user-status/", self.test_user_status_dict, format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            "/api/user-status/", {"from": "1990-01-01"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["user_statuses"]), 1)
        self._validate_data(response.data["user_statuses"][0], dt.date.today())

    # query parameters are valid, range test with 100 entries
    def test_list_user_statuses_valid_date_from_range(self):
        start_date = dt.date(2000, 1, 1)
        self._add_and_test_user_statuses(100, start_date)
        response = self.client.get(
            "/api/user-status/", {"from": "2000-01-01"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["user_statuses"]), 100)
        for i in range(100):
            self._validate_data(
                response.data["user_statuses"][i], start_date + dt.timedelta(days=i)
            )

    # query parameters are valid, range test with from and to date
    def test_list_user_statuses_valid_date_from_and_to_range(self):
        start_date = dt.date(2000, 1, 1)
        self._add_and_test_user_statuses(100, start_date)
        response = self.client.get(
            "/api/user-status/", {"from": "2000-01-01", "to": "2000-01-20"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["user_statuses"]), 20)
        for i in range(20):
            self._validate_data(
                response.data["user_statuses"][i], start_date + dt.timedelta(days=i)
            )

    # query parameters are valid, range test with from and to date, from date greater than to date
    def test_list_user_statuses_from_date_greater_than_to_date(self):
        start_date = dt.date(2000, 1, 1)
        self._add_and_test_user_statuses(100, start_date)
        response = self.client.get(
            "/api/user-status/", {"from": "2000-01-20", "to": "2000-01-10"}, follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["user_statuses"]), 0)

    ###########################################################################################################
    #                                  UserStatus "POST" method tests                                         #
    ###########################################################################################################

    # test if user is not authenticated
    def test_create_user_status_unauthenticated(self):
        self.client.logout()
        response = self.client.post(
            "/api/user-status/", self.test_user_status_dict, format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # data is invalid
    def test_create_user_status_invalid_data(self):
        self.test_user_status_dict.pop("mood")
        response = self.client.post(
            "/api/user-status/", self.test_user_status_dict, format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # data is valid
    def test_create_user_status_valid_data(self):
        response = self.client.post(
            "/api/user-status/", self.test_user_status_dict, format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._validate_data(response.data, dt.date.today())

    # data is valid and entry already exists
    def test_create_user_status_entry_exists(self):
        response = self.client.post(
            "/api/user-status/", self.test_user_status_dict, format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            "/api/user-status/", self.test_user_status_dict, format="json", follow=True
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # data is valid with different dates
    def test_create_user_status_different_dates(self):
        self._add_and_test_user_statuses(100, dt.date(2000, 1, 1))

    ###########################################################################################################
    #                                            Helper Functions                                             #
    ###########################################################################################################

    def _validate_data(self, response_data, date):
        self.assertGreaterEqual(response_data["id"], 1)
        self.assertEqual(response_data["date"], date.strftime("%Y-%m-%d"))
        self.assertEqual(response_data["mood"], self.test_user_status_dict["mood"])
        self.assertEqual(
            response_data["energy_level"], self.test_user_status_dict["energy_level"]
        )
        self.assertEqual(
            response_data["sleep_quality"], self.test_user_status_dict["sleep_quality"]
        )
        self.assertEqual(
            response_data["anxiety_level"], self.test_user_status_dict["anxiety_level"]
        )
        self.assertEqual(response_data["appetite"], self.test_user_status_dict["appetite"])
        self.assertEqual(response_data["content"], self.test_user_status_dict["content"])

    def _add_and_test_user_statuses(self, num_entries, start_date):
        self.client.logout()
        freezer = freeze_time(start_date)
        freezer.start()
        self.client.login(username="testuser", password="testpassword")
        for i in range(num_entries):
            response = self.client.post(
                "/api/user-status/", self.test_user_status_dict, format="json", follow=True
            )
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                self.client.login(username="testuser", password="testpassword")
                response = self.client.post(
                    "/api/user-status/",
                    self.test_user_status_dict,
                    format="json",
                    follow=True,
                )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self._validate_data(response.data, start_date + dt.timedelta(days=i))
            freezer.stop()
            freezer = freeze_time(start_date + dt.timedelta(days=i + 1))
            freezer.start()

        self.client.logout()
        freezer.stop()
        self.client.login(username="testuser", password="testpassword")
