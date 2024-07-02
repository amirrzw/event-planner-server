from django.urls import path
from .views import RegisterView, LoginView
from .custom_password_reset_views import CustomPasswordResetView, CustomPasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
