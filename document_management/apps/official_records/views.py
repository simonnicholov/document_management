from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from document_management.core.decorators import legal_required


@login_required
def index(request):
    context = {
        'title': 'Search Official Records',
    }
    return render(request, 'official_records/index.html', context)


@login_required
def lists(request, id):
    context = {
        'title': 'Search Official Records',
    }
    return render(request, 'official_records/lists.html', context)


@login_required
def details(request, id):
    context = {
        'title': 'Details Official Records',
    }
    return render(request, 'official_records/details.html', context)


@legal_required
def add(request, id=None):
    context = {
        'title': 'Add Official Records',
    }
    return render(request, 'official_records/add.html', context)


@legal_required
def edit(request, id=None):
    context = {
        'title': 'Edit Official Records',
    }
    return render(request, 'official_records/edit.html', context)


@legal_required
def delete(request, id=None):
    context = {
        'title': 'Delete Official Records',
    }
    return render(request, 'official_records/delete.html', context)


@legal_required
def upload(request, id=None):
    context = {
        'title': 'Upload Official Records',
    }
    return render(request, 'official_records/upload.html', context)


@legal_required
def preview(request, id=None):
    context = {
        'title': 'Preview Official Records',
    }
    return render(request, 'official_records/preview.html', context)


@legal_required
def change_record_status(request, id=None):
    context = {
        'title': 'Change Record Official Records',
    }
    return render(request, 'official_records/add.html', context)
