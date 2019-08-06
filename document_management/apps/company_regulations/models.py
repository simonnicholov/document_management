from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField

from document_management.core.utils import FilenameGenerator


class CompanyRegulation(models.Model):
    CATEGORY = Choices(
        (1, 'director_decisions', 'Director Decisions'),
        (2, 'circular_letter', 'Circular Letter'),
        (3, 'other', 'Other'),
    )

    TYPE = Choices(
        (1, 'private', 'Private'),
        (2, 'public', 'Public'),
    )

    location = models.ForeignKey('locations.Location', related_name="company_regulations",
                                 on_delete=models.CASCADE, blank=True, null=True)
    number = models.CharField(max_length=32)
    subject = models.CharField(max_length=64)
    effective_date = models.DateField()
    expired_date = models.DateField()

    category = models.PositiveSmallIntegerField(choices=CATEGORY)
    type = models.PositiveSmallIntegerField(choices=TYPE)

    total_document = models.IntegerField(default=0)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Number ({self.number}) : {self.subject}"


class CompanyRegulationFile(models.Model):
    document = models.OneToOneField('company_regulations.CompanyRegulation', related_name="company_regulation_files",
                                    on_delete=models.CASCADE)
    file = models.FileField(upload_to=FilenameGenerator('company_regulation_file'))
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.file.url)
