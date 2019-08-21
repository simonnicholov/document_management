from django import forms
from django.conf import settings
from django.core.validators import (MinValueValidator, MaxValueValidator,
                                    FileExtensionValidator)
from django.utils import timezone

from document_management.apps.documents.models import Document, DocumentLogs
from document_management.apps.locations.models import Location
from document_management.apps.partners.models import Partner

from document_management.core.choices import TYPE, CATEGORY, STATUS
from document_management.core.dictionaries import DICT_STATUSES
from document_management.core.attributes import get_select_attribute


select_widget = get_select_attribute()


class ContractForm(forms.Form):
    number = forms.CharField(max_length=32)
    effective_date = forms.DateField(input_formats=["%Y-%m-%d"])
    expired_date = forms.DateField(input_formats=["%Y-%m-%d"])
    subject = forms.CharField(max_length=64)
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True).order_by('name'),
        empty_label=settings.EMPTY_LABEL, widget=select_widget
    )
    category = forms.ChoiceField(choices=CATEGORY, widget=select_widget)
    type = forms.ChoiceField(choices=TYPE, widget=select_widget)
    description = forms.CharField(widget=forms.Textarea(), required=False)

    partner = forms.ModelChoiceField(
        queryset=Partner.objects.filter(is_active=True).order_by('name'),
        empty_label=settings.EMPTY_LABEL, widget=select_widget
    )
    amount = forms.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(settings.MAX_VALIDATOR_AMOUNT,
                                      (f'Can not greater than {settings.MAX_VALIDATOR_TEXT} '))
                    ])
    job_specification = forms.CharField(max_length=256)
    beginning_period = forms.DateField(input_formats=["%Y-%m-%d"])
    ending_period = forms.DateField(input_formats=["%Y-%m-%d"])
    retention_period = forms.IntegerField(min_value=1, max_value=7300, required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_category(self):
        if self.cleaned_data['category'] == "0":
            raise forms.ValidationError("Please select item in the list", code="field_is_required")

        return self.cleaned_data['category']

    def clean_type(self):
        if self.cleaned_data['type'] == "0":
            raise forms.ValidationError("Please select item in the list", code="field_is_required")

        return self.cleaned_data['type']

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        effective_date = cleaned_data['effective_date']
        expired_date = cleaned_data['expired_date']

        if effective_date > expired_date:
            raise forms.ValidationError("Effective date can not be greater than expired date",
                                        code="invalid_date_range")

        beginning_period = cleaned_data['beginning_period']
        ending_period = cleaned_data['ending_period']

        if beginning_period > ending_period:
            raise forms.ValidationError("Beginning period can not be greater than ending period",
                                        code="invalid_date_range")

        return cleaned_data

    def save(self, *args, **kwargs):
        number = self.cleaned_data['number']
        effective_date = self.cleaned_data['effective_date']
        expired_date = self.cleaned_data['expired_date']
        subject = self.cleaned_data['subject']
        location = self.cleaned_data['location']
        category = self.cleaned_data['category']
        type = self.cleaned_data['type']
        partner = self.cleaned_data['partner']
        amount = self.cleaned_data['amount']
        job_specification = self.cleaned_data['job_specification']
        beginning_period = self.cleaned_data['beginning_period']
        ending_period = self.cleaned_data['ending_period']

        # Mandatory, but this is hardcoded
        group = settings.GROUP_CONTRACT

        # Optional
        description = self.cleaned_data['description']
        retention_period = self.cleaned_data['retention_period']

        defaults = {
            'effective_date': effective_date,
            'expired_date': expired_date,
            'subject': subject,
            'location': location,
            'category': category,
            'type': type,
            'group': group,
            'description': description,
            'partner': partner,
            'amount': amount,
            'job_specification': job_specification,
            'beginning_period': beginning_period,
            'ending_period': ending_period,
            'retention_period': retention_period
        }

        document, created = Document.objects.update_or_create(number=number,
                                                              defaults=defaults)

        if created:
            action = DocumentLogs.ACTION.create_document
        else:
            action = DocumentLogs.ACTION.update_document

        DocumentLogs.objects.create(document_id=document.id,
                                    document_subject=subject,
                                    action=action,
                                    updated_by=self.user,
                                    updated_date=timezone.now())

        return document


class ChangeRecordStatusForm(forms.Form):

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def is_valid(self):
        return True

    def save(self, *args, **kwargs):
        if self.document.is_active:
            self.document.is_active = False
        else:
            self.document.is_active = True

        updated_by = self.user
        updated_date = timezone.now()
        action = DocumentLogs.ACTION.update_document_status
        value = self.document.is_active

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    action=action,
                                    value=value,
                                    updated_by=updated_by,
                                    updated_date=updated_date)

        self.document.save(update_fields=['is_active'])

        return self.document


class DeleteForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def save(self, *args, **kwargs):
        document_number = self.document.number

        reason = self.cleaned_data['reason']
        action = DocumentLogs.ACTION.delete_document
        updated_by = self.user
        updated_date = timezone.now()

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    reason=reason,
                                    action=action,
                                    updated_by=updated_by,
                                    updated_date=updated_date)

        self.document.delete()

        return document_number


class ChangeStatusForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS, widget=select_widget)
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def clean_status(self):
        if int(self.cleaned_data['status']) == self.document.status:
            raise forms.ValidationError("Please select status first",
                                        code="selected_is_required")
        return self.cleaned_data['status']

    def save(self, *args, **kwargs):
        reason = self.cleaned_data['reason']
        action = DocumentLogs.ACTION.update_document_status
        value = DICT_STATUSES[self.cleaned_data['status']]
        updated_by = self.user
        updated_date = timezone.now()

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    reason=reason,
                                    action=action,
                                    value=value,
                                    updated_by=updated_by,
                                    updated_date=updated_date)

        self.document.status = int(self.cleaned_data['status'])
        self.document.save(update_fields=['status'])

        return self.document


class UploadForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def save(self, *args, **kwargs):
        self.document.files.create(file=self.cleaned_data['file'])
        self.document.total_document = self.document.total_document + 1
        self.document.save(update_fields=['total_document'])

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    action=DocumentLogs.ACTION.upload_document,
                                    updated_by=self.user,
                                    updated_date=timezone.now())

        return self.document
