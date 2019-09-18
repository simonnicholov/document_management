from model_utils import Choices


TYPE = Choices(
    (0, '-', '--- select ---'),
    (1, 'private', 'Private'),
    (2, 'public', 'Public'),
)

DOCUMENT_CATEGORY = Choices(
    (0, '-', '--- select ---'),
    (1, 'construction', 'Construction'),
    (2, 'property', 'Property'),
    (5, 'other', 'Other'),
)

COMPANY_CATEGORY = Choices(
    (0, '-', '--- select ---'),
    (3, 'director_decisions', 'Director Decisions'),
    (4, 'circular_letter', 'Circular Letter'),
    (5, 'other', 'Other'),
)

STATUS = Choices(
    (0, '-', '--- select ---'),
    (1, 'ongoing', 'Ongoing'),
    (2, 'done', 'Done'),
    (3, 'expired', 'Expired'),
)

BUSINESS_SECTOR = Choices(
    (0, 'select', '--- select ---'),
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
