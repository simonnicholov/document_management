from django import forms
from django.conf import settings
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    FileExtensionValidator)
from django.utils import timezone

from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import DocumentLogs


class AddendumForm(forms.Form):
    number = forms.CharField(max_length=32)
    signature_date = forms.DateField(input_formats=["%Y-%m-%d"])
    effective_date = forms.DateField(input_formats=["%Y-%m-%d"])
    subject = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea(), required=False)

    amount = forms.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(settings.MAX_VALIDATOR_AMOUNT,
                                      (f'Can not greater than {settings.MAX_VALIDATOR_TEXT} '))
                    ])

    job_specification = forms.CharField(max_length=256)
    retention_period = forms.IntegerField(min_value=1, max_value=7300, required=False)

    def __init__(self, document, user, is_update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user
        self.is_update = is_update

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if not self.is_update:
            addendum_exist = Addendum.objects.filter(document=self.document,
                                                     number=cleaned_data['number']).exists()
            if addendum_exist:
                raise forms.ValidationError("Number addendum has already used. "
                                            "Please check number correctly.",
                                            code="number_has_already_used")

        addendum_signature_date = cleaned_data['signature_date']
        addendum_effective_date = cleaned_data['effective_date']

        self.expired_date = self.document.expired_date
        document_signature_date = self.document.signature_date
        document_effective_date = self.document.effective_date

        group = self.document.get_group_display().lower()

        if addendum_signature_date < document_signature_date:
            raise forms.ValidationError("Signature date addendum can not less than signature date %s"
                                        % group,
                                        code="invalid_date_range")

        if addendum_signature_date > addendum_effective_date:
            raise forms.ValidationError("Signature date addendum can not greater than effective date %s"
                                        % group,
                                        code="invalid_date_range")

        if addendum_effective_date < document_effective_date:
            raise forms.ValidationError("Effective date addendum can not less than effective date %s"
                                        % group,
                                        code="invalid_date_range")

        if addendum_effective_date > self.expired_date:
            raise forms.ValidationError("Effective date addendum can not greater than expired date %s"
                                        % group,
                                        code="invalid_date_range")

        return cleaned_data

    def save(self, *args, **kwargs):
        number = self.cleaned_data['number']
        signature_date = self.cleaned_data['signature_date']
        effective_date = self.cleaned_data['effective_date']
        expired_date = self.expired_date
        subject = self.cleaned_data['subject']
        amount = self.cleaned_data['amount']
        job_specification = self.cleaned_data['job_specification']

        # Optional
        description = self.cleaned_data['description']
        retention_period = self.cleaned_data['retention_period']

        defaults = {
            'subject': subject,
            'signature_date': signature_date,
            'effective_date': effective_date,
            'expired_date': expired_date,
            'description': description,
            'amount': amount,
            'job_specification': job_specification,
            'retention_period': retention_period
        }

        addendum, created = Addendum.objects.update_or_create(document=self.document, number=number,
                                                              defaults=defaults)

        if created:
            action = DocumentLogs.ACTION.create_addendum_relational
        else:
            action = DocumentLogs.ACTION.update_addendum_relational

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    addendum_id=addendum.id,
                                    addendum_subject=addendum.subject,
                                    action=action,
                                    updated_by=self.user,
                                    updated_date=timezone.now())

        return addendum


class ChangeRecordStatusForm(forms.Form):

    def __init__(self, addendum, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addendum = addendum
        self.user = user

    def is_valid(self):
        return True

    def save(self, *args, **kwargs):
        if self.addendum.is_active:
            self.addendum.is_active = False
        else:
            self.addendum.is_active = True

        updated_by = self.user
        updated_date = timezone.now()
        action = DocumentLogs.ACTION.update_addendum_relational_record_status
        value = self.addendum.is_active

        DocumentLogs.objects.create(document_id=self.addendum.document.id,
                                    document_subject=self.addendum.document.subject,
                                    addendum_id=self.addendum.id,
                                    addendum_subject=self.addendum.subject,
                                    action=action,
                                    value=value,
                                    updated_by=updated_by,
                                    updated_date=updated_date)

        self.addendum.save(update_fields=['is_active'])

        return self.addendum


class UploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __init__(self, addendum, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addendum = addendum
        self.user = user

    def save(self, *args, **kwargs):
        self.addendum.files.create(file=self.cleaned_data['file'])
        self.addendum.document.total_addendum = self.addendum.document.total_addendum + 1
        self.addendum.document.save(update_fields=['total_addendum'])

        DocumentLogs.objects.create(document_id=self.addendum.document.id,
                                    document_subject=self.addendum.document.subject,
                                    addendum_id=self.addendum.id,
                                    addendum_subject=self.addendum.subject,
                                    action=DocumentLogs.ACTION.upload_addendum_file_relational,
                                    updated_by=self.user,
                                    updated_date=timezone.now())

        return self.addendum


class DeleteForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, addendum, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addendum = addendum
        self.user = user

    def save(self, *args, **kwargs):
        addendum_number = self.addendum.number

        reason = self.cleaned_data['reason']
        action = DocumentLogs.ACTION.delete_addendum_relational
        updated_by = self.user
        updated_date = timezone.now()

        DocumentLogs.objects.create(document_id=self.addendum.document.id,
                                    document_subject=self.addendum.document.subject,
                                    addendum_id=self.addendum.id,
                                    reason=reason,
                                    action=action,
                                    updated_by=updated_by,
                                    updated_date=updated_date)

        self.addendum.delete()

        return addendum_number
