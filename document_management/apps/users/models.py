from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

from document_management.apps.permission_requests.models import PermissionRequest


class CustomUserManager(UserManager):

    def create_user(self, email, password, type=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        user = self.model(email=email, is_staff=False,
                          is_active=True, is_superuser=False,
                          last_login=now, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email,
                                password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True, null=True,
                              max_length=254, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    role = models.ForeignKey('role_permissions.Role', related_name="users",
                             on_delete=models.CASCADE, blank=True, null=True)

    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField('superuser status', default=False)
    is_active = models.BooleanField('active', default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_role_id(self) -> int:
        if self.role:
            return self.role.id
        return None

    def get_role_name(self) -> str:
        if self.role:
            return self.role.name
        return None

    def has_permission(self, document_id):
        user_request = self.user_requests\
            .filter(document__id=document_id, status=PermissionRequest.STATUS.approved).first()

        if not user_request:
            return False

        action_date = user_request.action_date + relativedelta(days=+1)
        today = timezone.now()

        if today > action_date:
            if not user_request.viewed_date:
                user_request.has_viewed = True
                user_request.viewed_date = timezone.now()
                user_request.save(update_fields=['has_viewed', 'viewed_date'])
                return True
            else:
                viewed_date = user_request.viewed_date + relativedelta(days=+1)

            if today < viewed_date:
                return True

            return False
        return True
