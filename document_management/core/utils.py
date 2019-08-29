import os

from datetime import datetime

from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.deconstruct import deconstructible


@deconstructible
class FilenameGenerator(object):
    """
    Utility class to handle generation of file upload path
    """
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, instance, filename):
        today = timezone.localtime(timezone.now()).date()

        filepath = os.path.basename(filename)
        filename, extension = os.path.splitext(filepath)
        filename = slugify(filename)

        path = "/".join([
            self.prefix,
            str(today.year),
            str(today.month),
            str(today.day),
            filename + extension
        ])
        return path


def prepare_datetime_range(start, end, tzinfo=None):
    """
    Function to ensure both start and end are timezone aware
    and ensure start starts at 0:0:0 and end ends at 23:59:59
    """
    start = convert_to_datetime(start, tzinfo)
    end = convert_to_datetime(end, tzinfo)

    # Peg the start date to start of the day, and end to end of the day
    start = start.replace(hour=00, minute=00, second=00)
    end = end.replace(hour=23, minute=59, second=59)

    return start, end


def convert_to_datetime(date, tzinfo=None):
    """
    Converts date objects into timezone aware datetime object
    """
    tzinfo = tzinfo or timezone.get_current_timezone()

    if isinstance(date, datetime):
        if timezone.is_naive(date):
            date = timezone.make_aware(date, tzinfo)

        return date

    return timezone.make_aware(datetime.datetime.combine(date, datetime.time()),
                               tzinfo)
