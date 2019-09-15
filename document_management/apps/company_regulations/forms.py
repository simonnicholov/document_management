from django import forms
from django.conf import settings
from django.utils import timezone

from document_management.apps.documents.models import (Document, DocumentLogs)
from document_management.core.attributes import get_select_attribute
from document_management.core.choices import COMPANY_CATEGORY


select_widget = get_select_attribute()


class CompanyRegulationForm(forms.Form):
    number = forms.CharField(max_length=32)
    subject = forms.CharField(max_length=64)
    effective_date = forms.DateField(input_formats=["%Y-%m-%d"])
    category = forms.ChoiceField(choices=COMPANY_CATEGORY, widget=select_widget)
    description = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_category(self):
        if self.cleaned_data['category'] == "0":
            raise forms.ValidationError("Please select item in the list", code="field_is_required")

        return self.cleaned_data['category']

    def save(self, *args, **kwargs):
        number = self.cleaned_data['number']
        subject = self.cleaned_data['subject']
        effective_date = self.cleaned_data['effective_date']
        category = self.cleaned_data['category']

        # Mandatory, but this is hardcoded
        group = settings.GROUP_COMPANY_REGULATION
        type = Document.TYPE.public

        # Optional
        description = self.cleaned_data['description']

        defaults = {
            'subject': subject,
            'effective_date': effective_date,
            'category': category,
            'group': group,
            'type': type,
            'description': description
        }

        document, created = Document.objects.update_or_create(number=number,
                                                              defaults=defaults)

        if created:
            action = DocumentLogs.ACTION.create_company_regulation
        else:
            action = DocumentLogs.ACTION.update_company_regulation

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
        action = DocumentLogs.ACTION.update_company_regulation_record_status
        value = self.document.is_active

        DocumentLogs.objects.create(document_id=self.document.id,
                                    document_subject=self.document.subject,
                                    action=action,
                                    value=value,
                                    updated_by=updated_by,
                                    updated_date=updated_date)

        self.document.save(update_fields=['is_active'])

        return self.document
