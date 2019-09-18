from django import forms

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

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_business_sector(self):
        if self.cleaned_data['business_sector'] == BUSINESS_SECTOR.select:
            raise forms.ValidationError("Please select business sector first",
                                        code="selected_is_required")
        return self.cleaned_data['business_sector']

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
                                                      director=director,
                                                      defaults=defaults)

        return partner
