from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from document_management.core.decorators import legal_required, user_required


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()

        if not user.role:
            messages.error(request, 'You do not have an access for this application !')
            return redirect('backoffice:login_view')

        login(request, user)

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            role_id = user.get_role_id()
            if role_id == settings.ROLE_SUPERUSER_ID or \
               role_id == settings.ROLE_LEGAL_ID:
                return redirect('backoffice:dashboard_legal')
            return redirect('backoffice:dashboard_user')
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect("login_view")


@legal_required
def dashboard_legal(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard_legal.html', context)


@user_required
def dashboard_user(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard_user.html', context)


@user_required
def permission_requests(request):
    context = {
        'title': 'Permission Requests'
    }
    return render(request, 'permission_requests.html', context)


@legal_required
def approval_requests(request):
    context = {
        'title': 'Approval Requests'
    }
    return render(request, 'approval_requests.html', context)


def change_password(request):
    context = {
        'title': 'Change Password'
    }
    return render(request, 'change_password.html', context)
