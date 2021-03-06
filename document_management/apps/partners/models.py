from django.db import models

from model_utils import Choices
from model_utils.fields import AutoCreatedField


class Partner(models.Model):
    BUSINESS_SECTOR = Choices(
        (1, 'aneka_industri', 'Aneka Industri'),
        (2, 'barang_konsumsi', 'Barang Konsumsi'),
        (3, 'industri_dasar_dan_kimia', 'Industri Dasar dan Kimia'),
        (4, 'infrastruktur', 'Infrastruktur'),
        (5, 'jasa', 'Jasa'),
        (6, 'keuangan', 'Keuangan'),
        (7, 'perdagangan', 'Perdagangan'),
        (8, 'pertambangan', 'Pertambangan'),
        (9, 'pertanian', 'Pertanian'),
        (10, 'properti', 'Properti'),
        (11, 'transportasi', 'Transportasi'),
    )

    name = models.CharField(max_length=64, unique=True, db_index=True)
    director = models.CharField(max_length=64, blank=True)
    person_in_charge = models.CharField(max_length=64, blank=True)
    business_sector = models.PositiveSmallIntegerField(choices=BUSINESS_SECTOR, blank=True, null=True)
    address = models.CharField(max_length=256)
    npwp = models.CharField(max_length=32, blank=True)
    siup = models.CharField(max_length=32, blank=True)
    ptkp = models.CharField(max_length=32, blank=True)
    telephone = models.CharField(max_length=32, blank=True)
    fax = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField('active', default=True)
    created = AutoCreatedField()

    def __str__(self):
        return self.name
