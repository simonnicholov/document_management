from django.db import models

from model_utils.fields import AutoCreatedField


class PermissionRequest(models.Model):
    documents = models.ForeignKey('documents.Document', related_name="documents",
                                  on_delete=models.CASCADE, blank=True, null=True)

    has_approved = models.BooleanField(default=False)
    user_approval = models.ForeignKey('users.User', related_name='user_approval',
                                      on_delete=models.CASCADE, blank=True, null=True)
    approved_date = models.DateTimeField()

    has_canceled = models.BooleanField(default=False)
    user_cancellation = models.ForeignKey('users.User', related_name='user_cancellation',
                                          on_delete=models.CASCADE, blank=True, null=True)
    canceled_date = models.DateTimeField()

    has_viewed = models.BooleanField(default=False)
    user_view = models.ForeignKey('users.User', related_name='user_view',
                                  on_delete=models.CASCADE, blank=True, null=True)
    viewed_date = models.DateTimeField()

    user_request = models.ForeignKey('users.User', related_name='user_request',
                                     on_delete=models.CASCADE)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Number ({self.number}) : {self.subject}"
