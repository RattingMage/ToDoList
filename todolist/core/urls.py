from django.urls import path
from core import views

urlpatterns = [
    path('signup', views, name="signup")
    path('login', views, name="login")
    path('profile', views, name="profile")
    path('update_password', views, name="update_password")
]