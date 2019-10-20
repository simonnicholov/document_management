from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class PermissionRequest(models.Model):
    document = models.ForeignKey('documents.Document', related_name="permission_requests",
                                 on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(default=None, max_length=256)

    STATUS = Choices(
        (1, 'approved', 'Approved'),
        (2, 'rejected', 'Rejected'),
        (3, 'request', 'Request'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.request)
    user_action = models.ForeignKey('users.User', related_name='user_action',
                                    on_delete=models.CASCADE, blank=True, null=True)
    action_reason = models.CharField(max_length=256, blank=True)
    action_date = models.DateTimeField(blank=True, null=True)

    has_viewed = models.BooleanField(default=False)
    viewed_date = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey('users.User', related_name='user_requests',
                             on_delete=models.CASCADE)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.id)
