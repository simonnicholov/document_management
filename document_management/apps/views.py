from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


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
            role_name = user.get_role_name()
            if role_name.lower() == settings.ROLE_SUPERUSER or \
               role_name.lower() == settings.ROLE_LEGAL:
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


def dashboard_legal(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard_legal.html', context)


def dashboard_user(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard_user.html', context)


def permission_requests(request):
    context = {
        'title': 'Permission Requests'
    }
    return render(request, 'permission_requests.html', context)


def approval_requests(request):
    context = {
        'title': 'Approval Requests'
    }
    return render(request, 'approval_requests.html', context)
