from django.db import models

from model_utils.fields import AutoCreatedField


class Location(models.Model):
    code = models.CharField(max_length=16, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    is_active = models.BooleanField(default=True)
    created = AutoCreatedField()

    def __str__(self):
        return self.name
