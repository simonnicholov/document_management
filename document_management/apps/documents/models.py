from django.core.validators import MinValueValidator
from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField

from document_management.core.utils import FilenameGenerator


class Document(models.Model):
    GROUP = Choices(
        (1, 'contract', 'Contract'),
        (2, 'mou', 'MoU'),
        (3, 'reading_news', 'Reading News'),
    )

    CATEGORY = Choices(
        (1, 'construction', 'Construction'),
        (2, 'property', 'Property'),
        (3, 'other', 'Other'),
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
    number = models.CharField(max_length=32, unique=True, db_index=True)
    subject = models.CharField(max_length=64)
    effective_date = models.DateField()
    expired_date = models.DateField()
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    group = models.PositiveSmallIntegerField(choices=GROUP)
    category = models.PositiveSmallIntegerField(choices=CATEGORY)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS.ongoing)

    job_specification = models.CharField(max_length=256, blank=True, null=True)
    beginning_period = models.DateField(blank=True, null=True)
    ending_period = models.DateField(blank=True, null=True)
    retention_period = models.PositiveSmallIntegerField(blank=True, null=True)

    total_document = models.PositiveSmallIntegerField(default=0)
    total_addendum = models.PositiveSmallIntegerField(default=0)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Number ({self.number}) : {self.subject}"


class DocumentFile(models.Model):
    document = models.ForeignKey('documents.Document', related_name="files",
                                 on_delete=models.CASCADE)
    file = models.FileField(upload_to=FilenameGenerator('document_file'))
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.file.url)


class DocumentLogs(models.Model):
    ACTION = Choices(
        (1, 'delete_record', 'Delete Record'),
        (2, 'document_status', 'Document Status'),
        (3, 'record_status', 'Record Status'),
    )
    document_id = models.IntegerField()
    document_subject = models.CharField(max_length=64)
    action = models.PositiveSmallIntegerField(choices=ACTION, blank=True, null=True)
    value = models.CharField(max_length=64, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    updated_by = models.ForeignKey('users.User', related_name="updated_logs",
                                   on_delete=models.CASCADE, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey('users.User', related_name="deleted_logs",
                                   on_delete=models.CASCADE, blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
