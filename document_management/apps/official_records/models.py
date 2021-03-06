from django.core.validators import MinValueValidator
from django.db import models

from model_utils.fields import AutoCreatedField

from document_management.core.utils import FilenameGenerator


class OfficialRecord(models.Model):
    document = models.ForeignKey('documents.Document', related_name="official_records",
                                 on_delete=models.CASCADE)
    number = models.CharField(max_length=64, unique=True, db_index=True)
    subject = models.CharField(max_length=256)
    signature_date = models.DateField(blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    expired_date = models.DateField(blank=True, null=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    description = models.TextField(blank=True)

    job_specification = models.CharField(max_length=256, blank=True)
    retention_period = models.PositiveSmallIntegerField(blank=True, null=True)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Number ({self.number}) : {self.subject}"


class OfficialRecordFile(models.Model):
    official_record = models.ForeignKey('official_records.OfficialRecord', related_name="files",
                                        on_delete=models.CASCADE)
    file = models.FileField(upload_to=FilenameGenerator('official_record_file'))
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.file.url)
