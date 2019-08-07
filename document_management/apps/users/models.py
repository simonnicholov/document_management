from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


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

    def get_role_name(self):
        if self.role:
            return self.role.name
        return None
