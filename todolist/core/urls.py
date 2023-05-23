from django.urls import path
from core.views import RegistrationView
from core.views import LoginView

urlpatterns = [
    path('signup', RegistrationView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name="login")
    # path('profile', views, name="profile")
    # path('update_password', views, name="update_password")
]