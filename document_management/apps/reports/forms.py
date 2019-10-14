import csv
import zipfile

from io import StringIO

from django import forms
from django.conf import settings

from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import Document
from document_management.apps.official_records.models import OfficialRecord
from document_management.core.utils import prepare_datetime_range


class ContractForm(forms.Form):
    start_date = forms.DateField(input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(input_formats=["%Y-%m-%d"])
    is_addendum = forms.BooleanField(required=False)
    is_official_record = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError("Start date can not be less than end date", code="invalid_date_range")

        return cleaned_data

    def generate_zip_response(self, http_response):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        date_range = str(start_date).replace('-', '') + '-' + \
            str(end_date).replace('-', '')
        start_date, end_date = prepare_datetime_range(start_date, end_date)
        response = http_response
        response['Content-Disposition'] = 'attachment; filename="%s-report-contract.zip"' \
            % date_range

        csv_filename = date_range + '-report-contract.csv'
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        documents = Document.objects.select_related('location', 'partner')\
                                    .filter(group=settings.GROUP_CONTRACT,
                                            expired_date__range=[start_date, end_date])\
                                    .order_by('-id')

        if self.cleaned_data['is_addendum'] or self.cleaned_data['is_official_record']:
            document_ids = list(documents.values_list('id', flat=True))

            if self.cleaned_data['is_addendum']:
                addendums = list(Addendum.objects.select_related('document')
                                                 .filter(document_id__in=document_ids)
                                                 .order_by('document_id', 'id'))
            if self.cleaned_data['is_official_record']:
                official_records = list(OfficialRecord.objects.select_related('document')
                                                      .filter(document_id__in=document_ids)
                                                      .order_by('document_id', 'id'))

        header = ('Number', 'Subject', 'Location', 'Partner', 'Category', 'Type', 'Amount', 'Expired Date')
        writer.writerow(header)

        for document in documents:
            writer.writerow([document.number, document.subject, document.location.name,
                             document.partner.name, document.get_category_display(),
                             document.get_type_display(), document.amount,
                             document.expired_date.strftime('%d-%b-%Y')])

            if document.total_addendum > 0 and self.cleaned_data['is_addendum']:
                current_addendums_list = addendums[0:document.total_addendum]
                header_addendum = ('', 'Number', 'Subject', 'Amount', 'Expired Date')
                writer.writerow(header_addendum)

                for addendum in current_addendums_list:
                    addendums.pop(0)
                    writer.writerow([None, addendum.number, addendum.subject, addendum.amount,
                                    addendum.expired_date.strftime('%d-%b-%y')])

            if document.total_official_record > 0 and self.cleaned_data['is_official_record']:
                current_official_record_list = official_records[0:document.total_official_record]
                header_official_record = ('', 'Number', 'Subject', 'Amount', 'Expired Date')
                writer.writerow(header_official_record)

                for official_record in current_official_record_list:
                    official_records.pop(0)
                    writer.writerow([None, official_record.number, official_record.subject,
                                     official_record.amount,
                                     official_record.expired_date.strftime('%d-%b-%y')])

        with zipfile.ZipFile(response, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(csv_filename, csv_buffer.getvalue())

        return response


class MoUForm(forms.Form):
    start_date = forms.DateField(input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(input_formats=["%Y-%m-%d"])
    is_addendum = forms.BooleanField(required=False)
    is_official_record = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError("Start date can not be less than end date", code="invalid_date_range")

        return cleaned_data

    def generate_zip_response(self, http_response):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        date_range = str(start_date).replace('-', '') + '-' + \
            str(end_date).replace('-', '')
        start_date, end_date = prepare_datetime_range(start_date, end_date)
        response = http_response
        response['Content-Disposition'] = 'attachment; filename="%s-report-mou.zip"' \
            % date_range

        csv_filename = date_range + '-report-mou.csv'
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        documents = Document.objects.select_related('location', 'partner')\
                                    .filter(group=settings.GROUP_MOU,
                                            expired_date__range=[start_date, end_date])\
                                    .order_by('-id')

        if self.cleaned_data['is_addendum'] or self.cleaned_data['is_official_record']:
            document_ids = list(documents.values_list('id', flat=True))

            if self.cleaned_data['is_addendum']:
                addendums = list(Addendum.objects.select_related('document')
                                                 .filter(document_id__in=document_ids)
                                                 .order_by('document_id', 'id'))
            if self.cleaned_data['is_official_record']:
                official_records = list(OfficialRecord.objects.select_related('document')
                                                      .filter(document_id__in=document_ids)
                                                      .order_by('document_id', 'id'))

        header = ('Number', 'Subject', 'Location', 'Partner', 'Category', 'Type', 'Amount', 'Expired Date')
        writer.writerow(header)

        for document in documents:
            writer.writerow([document.number, document.subject, document.location.name,
                             document.partner.name, document.get_category_display(),
                             document.get_type_display(), document.amount,
                             document.expired_date.strftime('%d-%b-%Y')])

            if document.total_addendum > 0 and self.cleaned_data['is_addendum']:
                current_addendums_list = addendums[0:document.total_addendum]
                header_addendum = ('', 'Number', 'Subject', 'Amount', 'Expired Date')
                writer.writerow(header_addendum)

                for addendum in current_addendums_list:
                    addendums.pop(0)
                    writer.writerow([None, addendum.number, addendum.subject, addendum.amount,
                                    addendum.expired_date.strftime('%d-%b-%y')])

            if document.total_official_record > 0 and self.cleaned_data['is_official_record']:
                current_official_record_list = official_records[0:document.total_official_record]
                header_official_record = ('', 'Number', 'Subject', 'Amount', 'Expired Date')
                writer.writerow(header_official_record)

                for official_record in current_official_record_list:
                    official_records.pop(0)
                    writer.writerow([None, official_record.number, official_record.subject,
                                     official_record.amount,
                                     official_record.expired_date.strftime('%d-%b-%y')])

        with zipfile.ZipFile(response, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(csv_filename, csv_buffer.getvalue())

        return response


class CompanyRegulationForm(forms.Form):
    start_date = forms.DateField(input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(input_formats=["%Y-%m-%d"])

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError("Start date can not be less than end date", code="invalid_date_range")

        return cleaned_data

    def generate_zip_response(self, http_response):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        date_range = str(start_date).replace('-', '') + '-' + \
            str(end_date).replace('-', '')
        start_date, end_date = prepare_datetime_range(start_date, end_date)
        response = http_response
        response['Content-Disposition'] = 'attachment; filename="%s-report-company-regulation.zip"' \
            % date_range

        csv_filename = date_range + '-report-company-regulation.csv'
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        documents = Document.objects.filter(group=settings.GROUP_COMPANY_REGULATION,
                                            effective_date__range=[start_date, end_date])\
                                    .order_by('-id')

        header = ('Number', 'Subject', 'Category', 'Type', 'Effective Date')
        writer.writerow(header)

        for document in documents:
            writer.writerow([document.number, document.subject, document.get_category_display(),
                             document.get_type_display(), document.effective_date.strftime('%d-%b-%Y')])

        with zipfile.ZipFile(response, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(csv_filename, csv_buffer.getvalue())

        return response


class OfficialRecordForm(forms.Form):
    start_date = forms.DateField(input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(input_formats=["%Y-%m-%d"])

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError("Start date can not be less than end date", code="invalid_date_range")

        return cleaned_data

    def generate_zip_response(self, http_response):
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        date_range = str(start_date).replace('-', '') + '-' + \
            str(end_date).replace('-', '')
        start_date, end_date = prepare_datetime_range(start_date, end_date)
        response = http_response
        response['Content-Disposition'] = 'attachment; filename="%s-report-official-record.zip"' \
            % date_range

        csv_filename = date_range + '-report-official-record.csv'
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        documents = Document.objects.select_related('location', 'partner')\
                                    .filter(group=settings.GROUP_OFFICIAL_RECORD,
                                            expired_date__range=[start_date, end_date])\
                                    .order_by('-id')

        header = ('Number', 'Subject', 'Location', 'Partner', 'Category', 'Type', 'Amount', 'Expired Date')
        writer.writerow(header)

        for document in documents:
            writer.writerow([document.number, document.subject, document.location.name,
                             document.partner.name, document.get_category_display(),
                             document.get_type_display(), document.amount,
                             document.expired_date.strftime('%d-%b-%Y')])

        with zipfile.ZipFile(response, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(csv_filename, csv_buffer.getvalue())

        return response
