from django.urls import path, include

# from brandAdmin import views
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterViewSet,
    LoginViewSet,
    GenerateOTPViewSet,
    VerifyOTPViewSet,
    ValidateOTPViewSet,
    DisableOTPViewSet,
)

router = DefaultRouter()

router.register("register", RegisterViewSet, basename="register")
router.register("logIn", LoginViewSet, basename="logIn")
router.register("otp/generate", GenerateOTPViewSet, basename="otp_generate")
router.register("otp/verify", VerifyOTPViewSet, basename="otp_verify")
router.register("otp/validate", ValidateOTPViewSet, basename="otp_validate")
router.register("otp/disable", DisableOTPViewSet, basename="otp_disable")


urlpatterns = [
    path("", include(router.urls)),
]
