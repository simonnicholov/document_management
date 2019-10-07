from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import (render, redirect, reverse, get_object_or_404)

from document_management.apps.addendums.models import Addendum, AddendumFile
from document_management.apps.documents.models import Document
from document_management.core.decorators import legal_required

from .forms import (AddendumForm, ChangeRecordStatusForm, UploadForm, DeleteForm)


@login_required
def index(request):
    query = request.GET.get('query', '')
    category = int(request.GET.get('category', 0))
    group = int(request.GET.get('group', 0))
    signature_date = request.GET.get('signature_date', '')

    if query or category > 0 or group > 0 or signature_date:
        addendums = Addendum.objects.select_related('document')

        if signature_date:
            signature_date = datetime.strptime(signature_date, '%Y-%m-%d').date()
            addendums = addendums.filter(signature_date=signature_date)
            signature_date = signature_date.strftime("%Y-%m-%d")

        if category > 0:
            addendums = addendums.filter(document__category=category)

        if group > 0:
            addendums = addendums.filter(document__group=group)

        if query:
            addendums = addendums.filter(Q(number__icontains=query) |
                                         Q(subject__icontains=query))

        addendums = addendums.order_by('-id')
    else:
        addendums = []

    page = request.GET.get('page', 1)

    paginator = Paginator(addendums, 25)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Search Addendums',
        'document': Document,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'query': query,
        'category': category,
        'group': group,
        'signature_date': signature_date
    }
    return render(request, 'addendums/index.html', context)


@login_required
def lists(request, id):
    document = get_object_or_404(Document, id=id)
    addendums = document.addendums.order_by('-id')

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

    user = request.user
    if user.get_role_id() == settings.ROLE_USER_ID and \
       addendum.document.type == Document.TYPE.private:
        if not user.has_permission(id):
            messages.error(request, "You do not have an access, but you can request an access.")
            return redirect(reverse("backoffice:permission_requests:requests",
                                    args=[addendum.document.id, addendum.document.group]))

    if addendum.is_active:
        addendum.record_status_class = "badge badge-success p-1 ml-1"
    else:
        addendum.record_status_class = "badge badge-danger p-1 ml-1"

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
        'signature_date': addendum.signature_date.strftime("%Y-%m-%d"),
        'effective_date': addendum.effective_date.strftime("%Y-%m-%d"),
        'description': addendum.description,
        'amount': addendum.amount,
        'job_specification': addendum.job_specification,
        'retention_period': addendum.retention_period
    }

    form = AddendumForm(data=request.POST or None, initial=initial,
                        document=addendum.document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, f'{addendum.number} has been updated')
        return redirect(reverse('backoffice:addendums:details', args=[addendum.id]))
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Edit Addendum',
        'addendum': addendum,
        'document': addendum.document,
        'form': form
    }
    return render(request, 'addendums/edit.html', context)


@legal_required
def delete(request, id):
    addendum = get_object_or_404(
        Addendum.objects.select_related('document')
                        .filter(is_active=True), id=id
    )

    if addendum.document.status == Document.STATUS.done:
        messages.error(request, "Addendum can not be deleted, the %s # %s status has already done"
                       % (addendum.document.get_group_display().lower(), addendum.document.number))
        return redirect(reverse("backoffice:addendums:details", args=[addendum.id]))

    form = DeleteForm(data=request.POST or None, addendum=addendum, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Addendum # %s has been deleted" % addendum.number)
        return redirect(reverse("backoffice:addendums:lists", args=[addendum.document.id]))

    context = {
        'title': 'Delete Addendum',
        'addendum': addendum,
        'form': form
    }
    return render(request, 'addendums/delete.html', context)


@legal_required
def upload(request, id):
    addendum = get_object_or_404(
        Addendum.objects.select_related('document')
                .filter(is_active=True), id=id
    )

    if addendum.document.status == Document.STATUS.done:
        messages.error(request, "Addendum can not be uploaded, the %s # %s status has already done"
                       % (addendum.document.get_group_display().lower(), addendum.document.number))
        return redirect(reverse("backoffice:addendums:details", args=[addendum.id]))

    form = UploadForm(data=request.POST or None, files=request.FILES or None,
                      addendum=addendum, user=request.user)

    if form.is_valid():
        addendum = form.save()
        messages.success(request, "Addendum # %s files has already uploaded" %
                         (addendum.number))
        return redirect(reverse("backoffice:addendums:details", args=[addendum.id]))

    context = {
        'title': 'Upload Addendum',
        'addendum': addendum,
        'form': form
    }
    return render(request, 'addendums/upload.html', context)


@login_required
def preview(request, id):
    addendum_file = get_object_or_404(AddendumFile, id=id)

    context = {
        'title': 'Preview Addendum',
        'addendum_file': addendum_file
    }
    return render(request, 'addendums/preview.html', context)


@legal_required
def change_record_status(request, id):
    addendum = get_object_or_404(Addendum.objects.select_related('document'), id=id)

    if addendum.document.status == Document.STATUS.done:
        messages.error(request, "Addendum can not be changed, the %s # %s status has already done"
                       % (addendum.document.get_group_display().lower(), addendum.document.number))
        return redirect(reverse("backoffice:addendums:details", args=[addendum.id]))

    form = ChangeRecordStatusForm(addendum=addendum, user=request.user)

    if form.is_valid():
        addendum = form.save()

        if addendum.is_active:
            string_status = "activated"
        else:
            string_status = "deactivated"

        messages.success(request, "Addendum # %s has been %s" % (addendum.number, string_status))
        return redirect(reverse("backoffice:addendums:lists", args=[addendum.document.id]))

    return redirect(reverse("backoffice:addendums:lists", args=[addendum.document.id]))
