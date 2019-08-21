from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import Document
from document_management.core.decorators import legal_required


@login_required
def index(request):
    context = {
        'title': 'Search Addendums'
    }
    return render(request, 'addendums/index.html', context)


@login_required
def lists(request, id):
    document = get_object_or_404(Document, id=id)
    addendums = document.addendums.filter(is_active=True)

    context = {
        'title': 'List Addendums',
        'addendums': addendums,
        'document': document
    }
    return render(request, 'addendums/lists.html', context)


@login_required
def details(request, id):
    context = {
        'title': 'Detail Addendum'
    }
    return render(request, 'addendums/details.html', context)


@legal_required
def add(request, id):
    context = {
        'title': 'Add Addendum'
    }
    return render(request, 'addendums/add.html', context)


@legal_required
def edit(request, id):
    context = {
        'title': 'Edit Addendum'
    }
    return render(request, 'addendums/edit.html', context)


@legal_required
def delete(request, id):
    context = {
        'title': 'Delete Addendum'
    }
    return render(request, 'addendums/delete.html', context)


@legal_required
def upload(request, id):
    context = {
        'title': 'Upload Addendum'
    }
    return render(request, 'addendums/upload.html', context)


@login_required
def preview(request, id):
    context = {
        'title': 'Preview Addendum'
    }
    return render(request, 'addendums/preview.html', context)


@legal_required
def update_record_status(request, id):
    context = {
        'title': 'Update Record Status'
    }
    return render(request, 'addendums/update_record_status.html', context)
