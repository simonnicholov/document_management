from django.shortcuts import render


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
