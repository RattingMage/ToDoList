from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from core.serializers import RegistrationSerializer, LoginSerializer

User = get_user_model()


class RegistrationSerializerTestCase(APITestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password": "testpassword",
            "password_repeat": "testpassword"
        }
        self.invalid_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "test@example.com",
            "password": "testpassword",
            "password_repeat": "differentpassword"
        }

    def test_validate_passwords_match(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "password_repeat": "testpassword",
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data["password"], "testpassword")
        self.assertEqual(validated_data["password_repeat"], "testpassword")

    def test_validate_passwords_mismatch(self):
        data = {
            "username": "testuser",
            "password": "testpassword1",
            "password_repeat": "testpassword2",
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        error_message = serializer.errors["non_field_errors"][0]
        self.assertEqual(error_message, "Password and repeated password is not equal")

    def test_registration_view_post_invalid(self):
        response = self.client.post(reverse('signup'), data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_view_post_valid(self):
        response = self.client.post(reverse('signup'), data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertTrue(check_password(self.valid_data['password'], user.password))

    def test_registration_view_permissions(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('signup'), data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.valid_user = User.objects.create_user(username='testuser', password='testpassword')
        self.serializer_data = {'username': self.valid_user.username, 'password': 'testpassword'}
        self.invalid_serializer_data = {'username': self.valid_user.username, 'password': 'invalidpassword'}

    def test_login_serializer_create_valid(self):
        serializer = LoginSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user, self.valid_user)

    def test_login_serializer_create_invalid(self):
        serializer = LoginSerializer(data=self.invalid_serializer_data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(AuthenticationFailed):
            serializer.save()

    def test_login_view_post_valid(self):
        self.client.force_authenticate(user=AnonymousUser())
        response = self.client.post(reverse('login'), data=self.serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.valid_user.username)

    def test_login_view_post_invalid(self):
        self.client.force_authenticate(user=AnonymousUser())
        response = self.client.post(reverse('login'), data=self.invalid_serializer_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_view_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('login'), data=self.serializer_data)

        self.assertEqual(response.status_code, 200)


class ProfileViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@test.com')
        self.client.force_authenticate(user=self.user)

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile'))
        self.client.force_authenticate(user=None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_profile_view_update(self):
        response = self.client.put(reverse('profile'),
                                   data={'first_name': 'John', 'last_name': 'Doe', 'username': self.user.username,
                                         'email': self.user.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_profile_view_delete(self):
        response = self.client.delete(reverse('profile'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile_view_not_authenticated(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(reverse('update_password'))
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_profile_view_csrf_cookie(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('csrftoken' in response.cookies)


class UpdatePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_update_password_view_valid(self):
        data = {
            'old_password': 'testpassword',
            'new_password': 'newtestpassword',
        }
        response = self.client.put(reverse('update_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword'))

    def test_update_password_view_invalid_old_password(self):
        data = {
            'old_password': 'incorrectpassword',
            'new_password': 'newtestpassword',
        }
        response = self.client.put(reverse('update_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpassword'))

    def test_update_password_view_not_authenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            'old_password': 'testpassword',
            'new_password': 'newtestpassword',
        }
        response = self.client.put(reverse('update_password'), data=data)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpassword'))

    def test_update_password_missing_fields(self):
        url = reverse('update_password')
        data = {}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
        self.assertIn('new_password', response.data)

    def test_update_password_method_not_allowed(self):
        url = reverse('update_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
