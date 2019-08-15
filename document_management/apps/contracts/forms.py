from django import forms
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

from document_management.apps.documents.models import Document, DocumentLogs
from document_management.apps.locations.models import Location
from document_management.apps.partners.models import Partner

from document_management.core.choices import TYPE, CATEGORY
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
            'number': number,
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
        print('defaults : ', defaults)

        document, _ = Document.objects.update_or_create(number=number,
                                                        defaults=defaults)

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
        self.document.save()

        updated_by = self.user
        updated_date = timezone.now()
        action = DocumentLogs.ACTION.record_status
        value = self.document.is_active

        self.document.logs.create(action=action, value=value,
                                  updated_by=updated_by, updated_date=updated_date)

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
        action = DocumentLogs.ACTION.delete_record
        deleted_by = self.user
        deleted_date = timezone.now()
        self.document.logs.create(reason=reason, action=action,
                                  deleted_by=deleted_by, deleted_date=deleted_date)
        self.document.delete()

        return document_number
