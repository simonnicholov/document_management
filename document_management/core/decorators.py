from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def legal_required(view_func):
    def _legal_required(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.info(request, 'You have to be logged in to view this page.')
            logout(request)
            return redirect_to_login(request.path_info)

        if request.user.get_role_id() == settings.ROLE_USER_ID:
            messages.info(request, 'You do not have an access to view this page')
            return redirect("backoffice:dashboard_user")

        return view_func(request, *args, **kwargs)
    return _legal_required


def user_required(view_func):
    def _user_required(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.info(request, 'You have to be logged in to view this page.')
            logout(request)
            return redirect_to_login(request.path_info)

        if request.user.get_role_id() != settings.ROLE_USER_ID:
            messages.info(request, 'You do not have an access to view this page')
            return redirect("backoffice:dashboard_legal")

        return view_func(request, *args, **kwargs)
    return _user_required
