from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserAccountUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('logout/', UserLogoutView.as_view(), name = 'logout'),
    path('profile/', UserAccountUpdateView.as_view(), name='update_profile'),
]