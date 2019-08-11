from model_utils import Choices


TYPE = Choices(
    (0, '-', '--- select ---'),
    (1, 'private', 'Private'),
    (2, 'public', 'Public'),
)

CATEGORY = Choices(
    (0, '-', '--- select ---'),
    (1, 'construction', 'Construction'),
    (2, 'property', 'Property'),
    (3, 'other', 'Other'),
)
