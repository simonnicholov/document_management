from django.conf import settings


def context_constant(request):
    context = {
        'ROLE_SUPERUSER_ID': settings.ROLE_SUPERUSER_ID,
        'ROLE_LEGAL_ID': settings.ROLE_LEGAL_ID,
        'ROLE_USER_ID': settings.ROLE_USER_ID
    }
    return context
