from django.db import models

from model_utils.fields import AutoCreatedField


class Permission(models.Model):
    name = models.CharField(max_length=32, unique=True)
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.name)
