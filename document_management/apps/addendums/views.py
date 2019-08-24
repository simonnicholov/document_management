from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (render, redirect, reverse, get_object_or_404)

from document_management.apps.addendums.models import Addendum
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
    addendum = get_object_or_404(
        Addendum.objects.select_related('document'), id=id
    )

    if request.user.get_role_id() == settings.ROLE_USER_ID and \
       addendum.document.type == Document.TYPE.private:
        messages.error(request, "You do not have an access, but you can request an access to the document first.")
        return redirect("backoffice:permission_requests")

    if addendum.document.type == Document.TYPE.private:
        addendum.badge_type = "badge badge-danger p-1"
    else:
        addendum.badge_type = "badge badge-success p-1"

    if addendum.document.status == Document.STATUS.ongoing:
        addendum.badge_status = "badge badge-warning p-1"
    elif addendum.document.status == Document.STATUS.done:
        addendum.badge_status = "badge badge-success p-1"
    elif addendum.document.status == Document.STATUS.expired:
        addendum.badge_status = "badge badge-danger p-1"

    context = {
        'title': 'Detail Addendum',
        'addendum': addendum,
        'document': addendum.document
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

    if form.is_valid():
        addendum = form.save()
        messages.success(request, f'{addendum.number} has been added')
        return redirect(reverse('backoffice:addendums:lists', args=[document.id]))
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
    addendum = get_object_or_404(
        Addendum.objects.select_related('document')
                .filter(is_active=True), id=id
    )

    if addendum.document.status == Document.STATUS.done:
        messages.error(request, "Addendum can not be change, the %s # %s status has already done"
                       % (addendum.document.get_group_display().lower(), addendum.document.number))
        return redirect(reverse("backoffice:addendums:details", args=[addendum.id]))

    initial = {
        'number': addendum.number,
        'subject': addendum.subject,
        'effective_date': addendum.effective_date.strftime("%Y-%m-%d"),
        'description': addendum.description,
        'amount': addendum.amount,
        'job_specification': addendum.job_specification,
        'beginning_period': addendum.beginning_period.strftime("%Y-%m-%d"),
        'ending_period': addendum.ending_period.strftime("%Y-%m-%d"),
        'retention_period': addendum.retention_period
    }

    form = AddendumForm(data=request.POST or None, initial=initial,
                        document=addendum.document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, f'{addendum.number} has been updated')
        return redirect(reverse('backoffice:addendums:details', args=[addendum.id]))

    context = {
        'title': 'Edit Addendum',
        'addendum': addendum,
        'document': addendum.document,
        'form': form
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
