from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from document_management.core.decorators import legal_required, user_required

from .forms import PasswordChangeForm


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()

        if not user.role:
            messages.error(request, 'You do not have an access for this application !')
            return redirect('backoffice:login')

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
    return redirect("backoffice:login")


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


@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your password has been successfully updated')
        # return redirect("backoffice:logout")

    context = {
        'form': form,
        'next': next,
        'title': 'Change Password',
    }
    return render(request, 'change_password.html', context)
