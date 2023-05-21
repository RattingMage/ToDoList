from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from core.serializers import RegistrationSerializer

USER_MODEL = get_user_model()


class RegistrationView(generics.CreateAPIView):
    model = USER_MODEL
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer
