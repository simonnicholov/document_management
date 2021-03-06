from django import forms

from document_management.apps.documents.models import Document
from document_management.apps.partners.models import Partner
from document_management.core.attributes import get_select_attribute
from document_management.core.choices import BUSINESS_SECTOR


select_widget = get_select_attribute()


class PartnerForm(forms.Form):
    name = forms.CharField(max_length=32)
    director = forms.CharField(max_length=64)
    person_in_charge = forms.CharField(max_length=64, required=False)
    business_sector = forms.ChoiceField(choices=BUSINESS_SECTOR, widget=select_widget)
    address = forms.CharField(widget=forms.Textarea(), required=False)
    npwp = forms.CharField(max_length=32, required=False)
    siup = forms.CharField(max_length=32, required=False)
    ptkp = forms.CharField(max_length=32, required=False)
    telephone = forms.CharField(max_length=32, required=False)
    fax = forms.CharField(max_length=32, required=False)

    def __init__(self, user, is_update=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.is_update = is_update

    def clean_business_sector(self):
        if int(self.cleaned_data['business_sector']) == BUSINESS_SECTOR.select:
            raise forms.ValidationError("Please select business sector first",
                                        code="selected_is_required")
        return self.cleaned_data['business_sector']

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if not self.is_update:
            if Partner.objects.filter(name=cleaned_data['name']).exists():
                raise forms.ValidationError("Name of Partner has already used. "
                                            "Please check name correctly.",
                                            code="name_has_already_used")

        return cleaned_data

    def save(self, *args, **kwargs):
        name = self.cleaned_data['name']
        director = self.cleaned_data['director']
        business_sector = self.cleaned_data['business_sector']

        # Optional
        person_in_charge = self.cleaned_data['person_in_charge']
        address = self.cleaned_data['address']
        npwp = self.cleaned_data['npwp']
        siup = self.cleaned_data['siup']
        ptkp = self.cleaned_data['ptkp']
        telephone = self.cleaned_data['telephone']
        fax = self.cleaned_data['fax']

        defaults = {
            'director': director,
            'business_sector': business_sector,
            'person_in_charge': person_in_charge,
            'address': address,
            'npwp': npwp,
            'siup': siup,
            'ptkp': ptkp,
            'telephone': telephone,
            'fax': fax
        }

        partner, _ = Partner.objects.update_or_create(name=name,
                                                      defaults=defaults)

        return partner


class ChangeRecordStatusForm(forms.Form):

    def __init__(self, partner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.partner = partner

    def is_valid(self):
        return True

    def save(self, *args, **kwargs):
        if self.partner.is_active:
            self.partner.is_active = False
        else:
            self.partner.is_active = True

        self.partner.save(update_fields=['is_active'])

        return self.partner


class DeleteForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea())

    def __init__(self, partner, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.partner = partner

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        has_used = Document.objects.filter(partner=self.partner).exists()
        if has_used:
            raise forms.ValidationError("Delete partner is not allowed, because partner has already used.",
                                        code="partner_has_used")

        return cleaned_data

    def save(self, *args, **kwargs):
        partner_name = self.partner.name
        self.partner.delete()

        return partner_name
