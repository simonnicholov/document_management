from django import forms
from django.conf import settings
from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.utils import timezone

from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import DocumentLogs


class AddendumForm(forms.Form):
    number = forms.CharField(max_length=32)
    effective_date = forms.DateField(input_formats=["%Y-%m-%d"])
    subject = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea(), required=False)

    amount = forms.FloatField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(settings.MAX_VALIDATOR_AMOUNT,
                                      (f'Can not greater than {settings.MAX_VALIDATOR_TEXT} '))
                    ])

    job_specification = forms.CharField(max_length=256)
    beginning_period = forms.DateField(input_formats=["%Y-%m-%d"])
    ending_period = forms.DateField(input_formats=["%Y-%m-%d"])
    retention_period = forms.IntegerField(min_value=1, max_value=7300, required=False)

    def __init__(self, document, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document
        self.user = user

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        effective_date = cleaned_data['effective_date']
        self.expired_date = self.document.expired_date

        if effective_date > self.expired_date:
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
        expired_date = self.expired_date
        subject = self.cleaned_data['subject']
        amount = self.cleaned_data['amount']
        job_specification = self.cleaned_data['job_specification']
        beginning_period = self.cleaned_data['beginning_period']
        ending_period = self.cleaned_data['ending_period']

        # Optional
        description = self.cleaned_data['description']
        retention_period = self.cleaned_data['retention_period']

        defaults = {
            'subject': subject,
            'effective_date': effective_date,
            'expired_date': expired_date,
            'description': description,
            'amount': amount,
            'job_specification': job_specification,
            'beginning_period': beginning_period,
            'ending_period': ending_period,
            'retention_period': retention_period
        }

        addendum, created = Addendum.objects.update_or_create(document=self.document, number=number,
                                                              defaults=defaults)

        if created:
            action = DocumentLogs.ACTION.create_addendum
        else:
            action = DocumentLogs.ACTION.update_adendum

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    addendum_id=addendum.id,
                                    addendum_subject=addendum.subject,
                                    action=action,
                                    updated_by=self.user,
                                    updated_date=timezone.now())

        return addendum
