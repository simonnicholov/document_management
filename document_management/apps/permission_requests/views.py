from django.shortcuts import render

from document_management.core.decorators import user_required


@user_required
def index(request):
    context = {
        'title': 'List Requests'
    }
    return render(request, 'permission_requests/index.html', context)


@user_required
def requests(request, id, type):
    context = {
        'title': 'Request Permission'
    }
    return render(request, 'permission_requests/requests.html', context)


@user_required
def details(request, id):
    context = {
        'title': 'Details Permission'
    }
    return render(request, 'permission_requests/details.html', context)
