from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from .serializers import RegistrationSerializer

User = get_user_model()


class RegistrationSerializerTestCase(APITestCase):
    def test_validate_passwords_match(self):
        data = {
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
            "password": "testpassword1",
            "password_repeat": "testpassword2",
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        error_message = serializer.errors["non_field_errors"][0]
        self.assertEqual(error_message, "Password and repeated password is not equal")

    def test_create_user(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
            "password_repeat": "testpassword",
            # Дополнительные поля, необходимые для создания пользователя
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))
        # Дополнительные проверки полей пользователя, если необходимо
