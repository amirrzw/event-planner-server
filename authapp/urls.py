from django.urls import path
from .views import RegisterView, LoginView, UserProfileView
from .custom_password_reset_views import CustomPasswordResetView, CustomPasswordResetConfirmView, ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='password_change'),
    path('user/', UserProfileView.as_view(), name='user_profile'),
]