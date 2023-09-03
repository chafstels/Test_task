from django.urls import path
from .views import RegistrationView, ActivationView, LoginView, UserListView, LogoutView, \
    ResetPasswordConfirmView, ResetPasswordView, UserProfileVIEW
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('list_user/', UserListView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view()),
    path('profile/', UserProfileVIEW.as_view()),
]
