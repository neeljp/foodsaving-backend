from django.contrib import auth
from rest_framework import status
from rest_framework.test import APITestCase
from yunity.users.factories import User


class TestUserAuthAPI(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User()
        cls.url = '/api/auth/'

    def test_login(self):
        data = {'email': self.user.email, 'password': self.user.display_name}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.user.email)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_no_credentials(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'email': ['This field is required.'],
                                         'password': ['This field is required.']})

    def test_wrong_credentials(self):
        data = {'email': self.user.email, 'password': 'wrong_password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Unable to login with provided credentials.', ])

    def test_status_not_logged_in(self):
        response = self.client.get('/api/auth/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['display_name'], '')

    def test_status_as_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/api/auth/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['display_name'], self.user.display_name)
