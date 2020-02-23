from django.conf import settings

from .enum import SortType


def context_constant(request):
    context = {
        'ROLE_SUPERUSER_ID': settings.ROLE_SUPERUSER_ID,
        'ROLE_LEGAL_ID': settings.ROLE_LEGAL_ID,
        'ROLE_USER_ID': settings.ROLE_USER_ID,
        'MESSAGE_SUCCESS': settings.MESSAGE_SUCCESS,
        'MESSAGE_ERROR': settings.MESSAGE_ERROR,
        'GROUP_CONTRACT': settings.GROUP_CONTRACT,
        'GROUP_MOU': settings.GROUP_MOU,
        'GROUP_OFFICIAL_RECORD': settings.GROUP_OFFICIAL_RECORD,
        'GROUP_COMPANY_REGULATION': settings.GROUP_COMPANY_REGULATION,
        'SORT_ASC': SortType.ASC.value,
        'SORT_DESC': SortType.DESC.value
    }
    return context
