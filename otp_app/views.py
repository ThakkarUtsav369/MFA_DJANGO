from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from otp_app.serializers import UserSerializer
from otp_app.models import UserModel
from rest_framework.viewsets import ModelViewSet
import pyotp


class RegisterViewSet(ModelViewSet):
    """
    API for Ragister User.

    # Sample Request Data
        {
            "email": "admin@admin.com",
            "name": "Admin",
            "password": "password123"
        }

    # Success Sample Response
        {
            "success": true,
            "message": "Registered successfully, please login",
            "payload": {
                "id": "c7bfa757-9e43-4393-ae8f-426fb1a8942a",
                "name": "Admin",
                "email": "admin@1gmail.com",
                "otp_enabled": false,
                "otp_verified": false,
                "otp_base32": null,
                "otp_auth_url": null
            }
        }
    # If email is already registered
        {
            "success": false,
            "message": {
                "email": [
                    "user with this email already exists."
                ]
            }
        }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    queryset = UserModel.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "Registered successfully, please login",
                        "payload": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except:
                return Response(
                    {
                        "success": False,
                        "message": "User with that email already exists",
                        "payload": [],
                    },
                    status=status.HTTP_409_CONFLICT,
                )
        else:
            return Response(
                {"success": False, "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginViewSet(ModelViewSet):
    """
    API for Login User.

    # Sample Request Data
        {
            "email": "admin@admin.com",
            "password": "password123"
        }
    # Success Sample Response
        {
            "success": true,
            "message": "User logged in successfully",
            "payload": {
                "id": "acb45ddd-3f75-4f68-b530-19ca6cc71959",
                "name": "Admin",
                "email": "admin@admin.com",
                "otp_enabled": false,
                "otp_verified": false,
                "otp_base32": null,
                "otp_auth_url": null
            }
        }
    # If email or password is wrong
        {
            "success": false,
            "message": "Incorrect email or password"
        }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    queryset = UserModel.objects.all()

    def create(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email.lower(), password=password)

        if user is None:
            return Response(
                {"success": False, "message": "Incorrect email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            return Response(
                {"success": False, "message": "Incorrect email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(user)
        return Response(
            {
                "success": True,
                "message": "User logged in successfully",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class GenerateOTPViewSet(ModelViewSet):
    """
    API for Generate OTP.

    # Sample Request Data
        {
            "user_id": "ba007454-e12d-4ba0-bece-ab304a1aa457",
            "email":"admin@admin.com"
        }
    # Success Sample Response
        {
            "success": true,
            "message": "OTP authentication url generated successfully",
            "base32": "4NE6ENX6G5JCHE3S4GYOZTROF6ILRVUU",
            "otpauth_url": "otpauth://totp/hikartech.in:admin%40admin.com?secret=4NE6ENX6G5JCHE3S4GYOZTROF6ILRVUU&issuer=hikartech.in"
        }
    # If user_id is wrong
        {
            "success": false,
            "message": "No user with Id: 8e9df9d6-1725-418f-9f28-d3a46952b23f found",
            "payload": []
        }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    queryset = UserModel.objects.all()

    def create(self, request):
        data = request.data
        user_id = data.get("user_id", None)
        email = data.get("email", None)

        user = UserModel.objects.filter(id=user_id).first()
        if user == None:
            return Response(
                {
                    "success": False,
                    "message": f"No user with Id: {user_id} found",
                    "payload": [],
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=email.lower(), issuer_name="hikartech.in"
        )

        user.otp_auth_url = otp_auth_url
        user.otp_base32 = otp_base32
        user.save()

        return Response(
            {
                "success": True,
                "message": "OTP authentication url generated successfully",
                "base32": otp_base32,
                "otpauth_url": otp_auth_url,
            },
            status=status.HTTP_200_OK,
        )


class VerifyOTPViewSet(ModelViewSet):
    """
    API for Varify OTP.

    # Sample Request Data
        {
            "user_id": "ba007454-e12d-4ba0-bece-ab304a1aa457",
            "token": "748344"
        }
    # Success Sample Response
        {
            "success": true,
            "message": "OTP is verified",
            "payload": {
                "id": "ba007454-e12d-4ba0-bece-ab304a1aa457",
                "name": "Demo",
                "email": "demo@gmail.com",
                "otp_enabled": true,
                "otp_verified": true,
                "otp_base32": "FAZCGUGOTDESSS4LMN7YAD4G73VMMEYY",
                "otp_auth_url": "otpauth://totp/hikartech.in:admin%40admin.com?secret=FAZCGUGOTDESSS4LMN7YAD4G73VMMEYY&issuer=hikartech.in"
            }
        }
    # If user_id is wrong
        {
            "success": false,
            "message": "No user with Id: ba007454-e12d-4ba0-bece-ab304a1aa457 found",
            "payload": []
        }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    queryset = UserModel.objects.all()

    def create(self, request):
        # message = "Token is invalid or user doesn't exist"
        data = request.data
        user_id = data.get("user_id", None)
        otp_token = data.get("token", None)
        user = UserModel.objects.filter(id=user_id).first()
        if user == None:
            return Response(
                {
                    "success": False,
                    "message": f"No user with Id: {user_id} found",
                    "payload": [],
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token):
            return Response(
                {
                    "success": False,
                    "message": "Token is invalid or user doesn't exist",
                    "payload": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.otp_enabled = True
        user.otp_verified = True
        user.save()
        serializer = self.serializer_class(user)

        return Response(
            {
                "success": True,
                "message": "OTP is verified",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ValidateOTPViewSet(ModelViewSet):
    """
    API for Varify OTP.

    # Sample Request Data
        {
            "user_id": "ba007454-e12d-4ba0-bece-ab304a1aa457",
            "token": "748344"
        }
    # Success Sample Response
        {
            "success": true,
            "message": "OTP token is valid"
        }
    # If user_id is wrong
        {
            "success": false,
            "message": "No user with Id: ba007454-e12d-4ba0-bece-ab304a1aa457 found",
            "payload": []
        }
    # If OTP is not varified
        {
            "success": false,
            "message": "OTP must be verified first",
            "payload": [],
        }
    # If token is wrong
        {
            "success": false,
            "message": "Token is invalid or user doesn't exist",
            "payload": []
        }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    queryset = UserModel.objects.all()

    def create(self, request):
        data = request.data
        user_id = data.get("user_id", None)
        otp_token = data.get("token", None)
        user = UserModel.objects.filter(id=user_id).first()
        if user == None:
            return Response(
                {
                    "success": False,
                    "message": f"No user with Id: {user_id} found",
                    "payload": [],
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not user.otp_verified:
            return Response(
                {
                    "success": False,
                    "message": "OTP must be verified first",
                    "payload": [],
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token, valid_window=1):
            return Response(
                {
                    "success": False,
                    "message": "Token is invalid or user doesn't exist",
                    "payload": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "OTP token is valid",
            },
            status=status.HTTP_200_OK,
        )


class DisableOTPViewSet(ModelViewSet):
    """
    API for Varify OTP.

    # Sample Request Data
        {
            "user_id": "ba007454-e12d-4ba0-bece-ab304a1aa457"
        }
    # Success Sample Response
        {
            "success": true,
            "message": "OTP disable successfully",
            "payload": {
                "id": "ba007454-e12d-4ba0-bece-ab304a1aa457",
                "name": "Demo",
                "email": "demo@gmail.com",
                "otp_enabled": false,
                "otp_verified": false,
                "otp_base32": null,
                "otp_auth_url": null
            }
        }
    # If user_id is wrong
        {
            "success": false,
            "message": "No user with Id: ba007454-e12d-4ba0-bece-ab304a1aa458 found",
            "payload": []
        }
    """

    serializer_class = UserSerializer
    http_method_names = ["post"]
    queryset = UserModel.objects.all()

    def create(self, request):
        data = request.data
        user_id = data.get("user_id", None)

        user = UserModel.objects.filter(id=user_id).first()
        if user == None:
            return Response(
                {
                    "success": False,
                    "message": f"No user with Id: {user_id} found",
                    "payload": [],
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user.otp_enabled = False
        user.otp_verified = False
        user.otp_base32 = None
        user.otp_auth_url = None
        user.save()
        serializer = self.serializer_class(user)

        return Response(
            {
                "success": True,
                "message": "OTP disable successfully",
                "payload": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
