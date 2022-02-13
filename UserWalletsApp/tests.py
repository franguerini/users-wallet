from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from UserWalletsApp.models import User, Wallet

# TODO: Add tests

class UserTests(APITestCase):
    def test_create_user(self):
        """
        Create an user creates
        """
        data = {"firstName": "test1", "lastName": "lastname", "password": "123456",  "email": "test@email.com", "alias": "alias123" }
        response = self.client.post("/user", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().firstName, "test1")
        self.assertEqual(User.objects.get().lastName, "lastname")
        self.assertEqual(User.objects.get().password, "123456")
        self.assertEqual(User.objects.get().email, "test@email.com")
        self.assertEqual(User.objects.get().alias, "alias123")

    def test_validate_unique_email(self):
        """
        Can't create a user with a repeated email
        """
        user1 = {"firstName": "user1", "lastName": "lastname", "password": "123456",  "email": "user@email.com", "alias": "alias" }
        user2 = {"firstName": "user2", "lastName": "lastname2", "password": "123456",  "email": "user@email.com", "alias": "alias" }
        # Create the first user
        response = self.client.post("/user", user1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.client.post("/user", user2, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
