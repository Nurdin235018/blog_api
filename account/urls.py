from django.urls import path
from .views import RegistrationView, ActivationView, LoginView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotConfirmPasswordView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('forgot-password-complete/', ForgotConfirmPasswordView.as_view())
]

