from django.urls import path, include # new added
from rest_framework.routers import DefaultRouter # new added

from .views import (
    RegisterView,
    Generate2FAView,
    GenerateQRCodeView,
    Verify2FAView,
    LoginView,
    MFALoginView,
    UserMeView, # new added
    UserViewSet, # new added
)

router = DefaultRouter() # new added
router.register('users', UserViewSet, basename='user') # new added

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    path("login/", LoginView.as_view(), name="login"),

    path("login/2fa/", MFALoginView.as_view(), name="login-2fa"),

    path("2fa/setup/", Generate2FAView.as_view(), name="2fa-setup"),

    path("2fa/qr/", GenerateQRCodeView.as_view(), name="2fa-qr"),

    path("2fa/verify/", Verify2FAView.as_view(), name="2fa-verify"),

    path("me/", UserMeView.as_view(), name="user-me"), # new added

    path('', include(router.urls)), # new added
]