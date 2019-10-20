from django.core.validators import MinValueValidator
from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField

from document_management.apps.users.models import User
from document_management.apps.permission_requests.models import PermissionRequest
from document_management.core.utils import FilenameGenerator


class Document(models.Model):
    GROUP = Choices(
        (1, 'contract', 'Contract'),
        (2, 'mou', 'MoU'),
        (3, 'official_record', 'Offical Record'),
        (4, 'company_regulation', 'Company Regulation'),
    )

    CATEGORY = Choices(
        (1, 'construction', 'Construction'),
        (2, 'property', 'Property'),
        (3, 'director_decisions', 'Director Decisions'),
        (4, 'circular_letter', 'Circular Letter'),
        (5, 'other', 'Other'),
    )

    TYPE = Choices(
        (1, 'private', 'Private'),
        (2, 'public', 'Public'),
    )

    STATUS = Choices(
        (1, 'ongoing', 'Ongoing'),
        (2, 'done', 'Done'),
        (3, 'expired', 'Expired'),
    )

    partner = models.ForeignKey('partners.Partner', related_name="documents",
                                on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey('locations.Location', related_name="documents",
                                 on_delete=models.CASCADE, blank=True, null=True)
    number = models.CharField(max_length=64, unique=True, db_index=True)
    subject = models.CharField(max_length=256)
    signature_date = models.DateField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    expired_date = models.DateField(blank=True, null=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    description = models.TextField(blank=True)

    group = models.PositiveSmallIntegerField(choices=GROUP)
    category = models.PositiveSmallIntegerField(choices=CATEGORY)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.ongoing)

    job_specification = models.CharField(max_length=256, blank=True)
    retention_period = models.PositiveSmallIntegerField(blank=True, null=True)

    total_document = models.PositiveSmallIntegerField(default=0)
    total_addendum = models.PositiveSmallIntegerField(default=0)
    total_official_record = models.PositiveSmallIntegerField(default=0)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Number ({self.number}) : {self.subject}"

    def validate_request_permission(self, user: User) -> bool:
        return self.permission_requests\
            .filter(user=user, status=PermissionRequest.STATUS.request).exists()


class DocumentFile(models.Model):
    document = models.ForeignKey('documents.Document', related_name="files",
                                 on_delete=models.CASCADE)
    file = models.FileField(upload_to=FilenameGenerator('document_file'))
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        if self.file:
            return str(self.file.url)
        return self.document.number


class DocumentLogs(models.Model):
    ACTION = Choices(
        # Contract
        (1, 'create_contract', 'Create Contract'),
        (2, 'update_contract', 'Update Contract'),
        (3, 'delete_contract', 'Delete Contract'),
        (4, 'upload_contract_file', 'Upload Contract File'),
        (5, 'delete_contract_file', 'Delete Contract File'),
        (6, 'update_contract_status', 'Update Contract Status'),
        (7, 'update_contract_record_status', 'Update Contract Record Status'),

        # MoU
        (11, 'create_mou', 'Create MoU'),
        (12, 'update_mou', 'Update MoU'),
        (13, 'delete_mou', 'Delete MoU'),
        (14, 'upload_mou_file', 'Upload MoU File'),
        (15, 'delete_mou_file', 'Delete MoU File'),
        (16, 'update_mou_status', 'Update MoU Status'),
        (17, 'update_mou_record_status', 'Update MoU Record Status'),

        # Official Record
        (21, 'create_official_record', 'Create Official Record'),
        (22, 'update_official_record', 'Update Official Record'),
        (23, 'delete_official_record', 'Delete Official Record'),
        (24, 'upload_official_record_file', 'Upload Official Record File'),
        (25, 'delete_official_record_file', 'Delete Official Record File'),
        (26, 'update_official_record_status', 'Update Official Record Status'),
        (27, 'update_official_record_record_status', 'Update Offical Record Record Status'),

        # Company Regulation
        (31, 'create_company_regulation', 'Create Company Regulation'),
        (32, 'update_company_regulation', 'Update Company Regulation'),
        (33, 'delete_company_regulation', 'Delete Company Regulation'),
        (34, 'upload_company_regulation_file', 'Upload Company Regulation File'),
        (35, 'delete_company_regulation_file', 'Delete Company Regulation File'),
        (36, 'update_company_regulation_status', 'Update Company Regulation Status'),
        (37, 'update_company_regulation_record_status', 'Update Company Regulation Record Status'),

        # Addendum Relational
        (41, 'create_addendum_relational', 'Create Addendum Relational'),
        (42, 'update_addendum_relational', 'Update Addendum Relational'),
        (43, 'delete_addendum_relational', 'Delete Addendum Relational'),
        (44, 'upload_addendum_relational_file', 'Upload Addendum Relational File'),
        (45, 'delete_addendum_relational_file', 'Delete Addendum Relational File'),
        (46, 'update_addendum_relational_record_status', 'Update Addendum Relational Record Status'),

        # Official Record Relational
        (51, 'create_official_record_relational', 'Create Official Record Relational'),
        (52, 'update_official_record_relational', 'Update Official Record Relational'),
        (53, 'delete_official_record_relational', 'Delete Official Record Relational'),
        (54, 'upload_official_record_relational_file', 'Upload Official Record Relational File'),
        (55, 'delete_official_record_relational_file', 'Delete Official Record Relational File'),
        (56, 'update_official_record_relational_record_status', 'Update Official Record Relational Record Status')
    )
    document_id = models.IntegerField(blank=True, null=True)
    document_subject = models.CharField(max_length=64, blank=True, null=True)
    addendum_id = models.IntegerField(blank=True, null=True)
    addendum_subject = models.CharField(max_length=64, blank=True, null=True)
    official_record_id = models.IntegerField(blank=True, null=True)
    official_record_subject = models.CharField(max_length=64, blank=True, null=True)
    action = models.PositiveSmallIntegerField(choices=ACTION, blank=True, null=True)
    value = models.CharField(max_length=64, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    updated_by = models.ForeignKey('users.User', related_name="updated_logs",
                                   on_delete=models.CASCADE, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
