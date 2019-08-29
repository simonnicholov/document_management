from django import forms
from django.utils import timezone

# from document_management.apps.permission_requests.models import PermissionRequest


class RequestPermissionForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def save(self, *args, **kwargs):
        # if self.document.is_active:
        #     self.document.is_active = False
        # else:
        #     self.document.is_active = True

        # updated_by = self.user
        # updated_date = timezone.now()
        # action = DocumentLogs.ACTION.update_contract_record_status
        # value = self.document.is_active

        # DocumentLogs.objects.create(document_id=self.document.id,
        #                             document_subject=self.document.subject,
        #                             action=action,
        #                             value=value,
        #                             updated_by=updated_by,
        #                             updated_date=updated_date)

        # self.document.save(update_fields=['is_active'])
        self.document.permission_requests.create(reason=self.cleaned_data['reason'],
                                                 user_request=self.user)

        return self.document
