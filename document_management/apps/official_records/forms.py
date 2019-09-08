from django import forms
from django.conf import settings
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.utils import timezone

from document_management.apps.documents.models import (Document, DocumentLogs)
from document_management.apps.locations.models import Location
from document_management.apps.partners.models import Partner

from document_management.core.attributes import get_select_attribute
from document_management.core.choices import TYPE, DOCUMENT_CATEGORY


select_widget = get_select_attribute()


class UnrelatedOfficialRecordForm(forms.Form):
    number = forms.CharField(max_length=32)
    signature_date = forms.DateField(input_formats=["%Y-%m-%d"])
    effective_date = forms.DateField(input_formats=["%Y-%m-%d"])
    expired_date = forms.DateField(input_formats=["%Y-%m-%d"])
    subject = forms.CharField(max_length=64)
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(is_active=True).order_by('name'),
        empty_label=settings.EMPTY_LABEL, widget=select_widget
    )
    category = forms.ChoiceField(choices=DOCUMENT_CATEGORY, widget=select_widget)
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

        signature_date = cleaned_data['signature_date']
        effective_date = cleaned_data['effective_date']
        expired_date = cleaned_data['expired_date']

        if signature_date > effective_date:
            raise forms.ValidationError("Signature date can not be greater than effective date",
                                        code="invalid_date_range")

        if effective_date > expired_date:
            raise forms.ValidationError("Effective date can not be greater than expired date",
                                        code="invalid_date_range")

        return cleaned_data

    def save(self, *args, **kwargs):
        number = self.cleaned_data['number']
        signature_date = self.cleaned_data['signature_date']
        effective_date = self.cleaned_data['effective_date']
        expired_date = self.cleaned_data['expired_date']
        subject = self.cleaned_data['subject']
        location = self.cleaned_data['location']
        category = self.cleaned_data['category']
        type = self.cleaned_data['type']
        partner = self.cleaned_data['partner']
        amount = self.cleaned_data['amount']
        job_specification = self.cleaned_data['job_specification']

        # Mandatory, but this is hardcoded
        group = settings.GROUP_OFFICIAL_RECORD

        # Optional
        description = self.cleaned_data['description']
        retention_period = self.cleaned_data['retention_period']

        defaults = {
            'signature_date': signature_date,
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
            'retention_period': retention_period
        }

        document, created = Document.objects.update_or_create(number=number,
                                                              defaults=defaults)

        if created:
            action = DocumentLogs.ACTION.create_contract
        else:
            action = DocumentLogs.ACTION.update_contract

        DocumentLogs.objects.create(document_id=document.id,
                                    document_subject=subject,
                                    action=action,
                                    updated_by=self.user,
                                    updated_date=timezone.now())

        return document
