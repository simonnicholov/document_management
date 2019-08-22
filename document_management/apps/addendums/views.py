from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import Document
from document_management.core.decorators import legal_required

from .forms import (AddendumForm)


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
    document = get_object_or_404(
        Document.objects.filter(is_active=True), id=id
    )

    if document.type == Document.TYPE.private:
        document.badge_type = "badge badge-danger p-1"
    else:
        document.badge_type = "badge badge-success p-1"

    if document.status == Document.STATUS.ongoing:
        document.badge_status = "badge badge-warning p-1"
    elif document.status == Document.STATUS.done:
        document.badge_status = "badge badge-success p-1"
    elif document.status == Document.STATUS.expired:
        document.badge_status = "badge badge-danger p-1"

    form = AddendumForm(data=request.POST or None, document=document,
                        user=request.user)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        addendum = form.save()
        messages.success(request, f'{addendum.number} has been added')
        return redirect('backoffice:contracts:index')
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Add Addendum',
        'form': form,
        'document': document
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
