from django.db import models

from model_utils.fields import AutoCreatedField

from document_management.core.utils import FilenameGenerator


class Addendum(models.Model):
    document = models.ForeignKey('documents.Document', related_name="addendums",
                                 on_delete=models.CASCADE)
    number = models.CharField(max_length=32)
    subject = models.CharField(max_length=64)
    effective_date = models.DateField(blank=True, null=True)
    expired_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return f"Number ({self.number}) : {self.subject}"


class AddendumFile(models.Model):
    addendum = models.OneToOneField('addendums.Addendum', related_name="addendum_files",
                                    on_delete=models.CASCADE)
    file = models.FileField(upload_to=FilenameGenerator('addendum_file'))
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return str(self.file.url)
