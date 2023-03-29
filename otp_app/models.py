import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserManager(BaseUserManager):
    """
    User manager class to handle user creation
    """

    def create_user(self, email, username,password=None, **extra_fields):
        """
        Creates a new User
          - Normalizes the email
          - Also creates a new auth token for the user
        """

        # Check if email is provided
        if not email:
            raise ValueError("User must have a valid email")

        # Normalize the provided email
        # email = self.normalize_email(email)

        # Creating user object
        # Default email isn't verified. To get it verified via email link
        user = self.model(email=email, is_active=True, **extra_fields)
        # # setting user password

        user.set_password(password)
        user.username = username
        # # saving user in database
        user.save()

        # generate token for user
        # Token.objects.create(user=user)
        return user

    def create_superuser(self, email,password=None, **extra_fields):
        """
        Creates a superuser
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    # password = models.CharField(max_length=32)
    otp_enabled = models.BooleanField(default=False)
    otp_verified = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=255, null=True)
    otp_auth_url = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name','username']

#     def get_absolute_url(self):
#         return reverse("users:detail", kwargs={"username": self.username})


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
