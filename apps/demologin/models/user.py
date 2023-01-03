from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone


DATETIME_FORMAT = settings.DATETIME_INPUT_FORMATS[0]
TIME_FORMAT = settings.TIME_INPUT_FORMATS[0]
DATE_FORMAT = settings.DATE_INPUT_FORMATS[0]

TOKEN_EXPIRE_TIME = 900  # 15 minutes
CACHE_EXPIRE_TIME = 900

NOTIFICATION_BODY = "ReCustomerに返品リクエストが届きました。"
NOTIFICATION_BODY_CANCEL = "ReCustomerにキャンセルリクエストが届きました。"


class UserRole(models.IntegerChoices):
    EMPLOYEE = 1
    MANAGER = 2
    ADMIN = 3
    MASTER_ADMIN = 4


class TimeStampMixin(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", UserRole.ADMIN)
        assert (
            extra_fields.get("role") == UserRole.ADMIN
        ), f"Superuser must have type={UserRole.ADMIN}."
        return self._create_user(email, password, **extra_fields)


def return_profile_upload_path(instance, filename):
    return f'user/profile/{filename}'


class User(AbstractBaseUser, TimeStampMixin):
    name = models.CharField(max_length=128, default="")
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(
        choices=UserRole.choices, default=UserRole.EMPLOYEE
    )
    profile = models.ImageField(
        upload_to=return_profile_upload_path, default=None, null=True, blank=True
    )
    reset_password_token = models.CharField(max_length=255, default=None, null=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        indexes = [
            models.Index(fields=["email"], name="email_idx"),
        ]

    def __str__(self):
        return self.email
