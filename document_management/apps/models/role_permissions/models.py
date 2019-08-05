from django.db import models

from model_utils.fields import AutoCreatedField


class Role(models.Model):
    name = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.name)


class Permission(models.Model):
    name = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.name)


class RolePermission(models.Model):
    role = models.ForeignKey('role_permissions.Role', related_name="role_permissions",
                             on_delete=models.CASCADE)
    permission = models.ForeignKey('role_permissions.Permission', related_name="role_permissions",
                                   on_delete=models.CASCADE)
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Role Permission #{self.id} : Role ({self.role.id}), Permission ({self.permission.id})"
