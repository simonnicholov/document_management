from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


# region external
def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
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


# region internal
def index(request):
    context = {
        'title': 'User'
    }
    return render(request, 'users/index.html', context)


def add(request):
    context = {
        'title': 'Add User'
    }
    return render(request, 'users/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit User'
    }
    return render(request, 'users/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete User'
    }
    return render(request, 'users/delete.html', context)


def details(request, id):
    context = {
        'title': 'Details User'
    }
    return render(request, 'users/details.html', context)


def reset_password(request, id):
    context = {
        'title': 'Reset Password'
    }
    return render(request, 'users/reset_password.html', context)
