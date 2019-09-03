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
)

STATUS = Choices(
    (0, '-', '--- select ---'),
    (1, 'ongoing', 'Ongoing'),
    (2, 'done', 'Done'),
    (3, 'expired', 'Expired'),
)
