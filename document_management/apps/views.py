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
            return redirect('backoffice:dashboard')
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect("login_view")


def dashboard(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard.html', context)


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
