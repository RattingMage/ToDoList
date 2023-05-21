from django.urls import path
from core.views import RegistrationView

urlpatterns = [
    path('signup', RegistrationView.as_view(), name="signup")
    # path('login', views, name="login")
    # path('profile', views, name="profile")
    # path('update_password', views, name="update_password")
]