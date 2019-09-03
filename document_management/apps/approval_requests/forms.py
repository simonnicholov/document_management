from django import forms
from django.utils import timezone

from document_management.apps.permission_requests.models import PermissionRequest


class ApproveForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, permission_request, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_request = permission_request
        self.user = user

    def save(self, *args, **kwargs):
        reason = self.cleaned_data['reason'] if self.cleaned_data['reason'] else None

        self.permission_request.status = PermissionRequest.STATUS.approved
        self.permission_request.action_reason = reason
        self.permission_request.user_action = self.user
        self.permission_request.action_date = timezone.now()
        self.permission_request.save(update_fields=['status', 'action_reason',
                                                    'user_action', 'action_date'])

        return self.permission_request


class RejectForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, permission_request, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permission_request = permission_request
        self.user = user

    def save(self, *args, **kwargs):
        self.permission_request.status = PermissionRequest.STATUS.rejected
        self.permission_request.action_reason = self.cleaned_data['reason']
        self.permission_request.user_action = self.user
        self.permission_request.action_date = timezone.now()
        self.permission_request.save(update_fields=['status', 'action_reason',
                                                    'user_action', 'action_date'])

        return self.permission_request
