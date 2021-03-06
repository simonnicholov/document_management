from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404

from document_management.apps.documents.models import Document, DocumentFile
from document_management.core.decorators import legal_required

from .forms import (MousForm, DeleteForm, ChangeRecordStatusForm,
                    ChangeStatusForm, UploadForm, RemoveForm)


@login_required
def index(request):
    query = request.GET.get('query', '')
    category = int(request.GET.get('category', 0))
    type = int(request.GET.get('type', 0))
    status = int(request.GET.get('status', 0))

    documents = Document.objects.select_related('partner')\
        .filter(group=settings.GROUP_MOU)

    if query:
        documents = documents.filter(Q(number__icontains=query) |
                                     Q(subject__icontains=query) |
                                     Q(partner__name__icontains=query))

    if category > 0:
        documents = documents.filter(category=category)

    if type > 0:
        documents = documents.filter(type=type)

    if status > 0:
        documents = documents.filter(status=status)

    documents = documents.order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(documents, 25)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    for document in page.object_list:
        if document.type == Document.TYPE.private:
            document.badge_type_class = "badge badge-danger p-1"
        else:
            document.badge_type_class = "badge badge-success p-1"

        if document.status == Document.STATUS.ongoing:
            document.badge_status_class = "badge badge-warning p-1"
        elif document.status == Document.STATUS.done:
            document.badge_status_class = "badge badge-success p-1"
        else:
            document.badge_status_class = "badge badge-danger p-1"

    context = {
        'title': 'Contract',
        'document': Document,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'query': query,
        'category': category,
        'type': type,
        'status': status
    }
    return render(request, 'mous/index.html', context)


@legal_required
def add(request):
    form = MousForm(data=request.POST or None, user=request.user)

    if form.is_valid():
        mou = form.save()
        messages.success(request, f'{mou.number} has been added')
        return redirect('backoffice:mous:index')
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Add MoU',
        'form': form
    }
    return render(request, 'mous/add.html', context)


@legal_required
def edit(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:mous:details", args=[document.id]))

    initial = {
        'number': document.number,
        'subject': document.subject,
        'signature_date': document.signature_date.strftime("%Y-%m-%d"),
        'effective_date': document.effective_date.strftime("%Y-%m-%d"),
        'expired_date': document.expired_date.strftime("%Y-%m-%d"),
        'location': document.location,
        'category': document.category,
        'type': document.type,
        'description': document.description,
        'partner': document.partner,
        'amount': document.amount,
        'job_specification': document.job_specification,
        'retention_period': document.retention_period
    }

    form = MousForm(data=request.POST or None, initial=initial, user=request.user,
                    is_update=True)

    if form.is_valid():
        form.save()
        messages.success(request, f'{document.number} has been updated')
        return redirect(reverse('backoffice:mous:details', args=[document.id]))

    context = {
        'title': 'Edit MoU',
        'document': document,
        'form': form
    }
    return render(request, 'mous/edit.html', context)


@legal_required
def delete(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:mous:details", args=[document.id]))

    if document.status == Document.STATUS.ongoing:
        document.badge_status_class = "badge badge-warning p-1"
    elif document.status == Document.STATUS.done:
        document.badge_status_class = "badge badge-success p-1"
    elif document.status == Document.STATUS.expired:
        document.badge_status_class = "badge badge-danger p-1"

    form = DeleteForm(data=request.POST or None, document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s has been deleted" % document.number)
        return redirect("backoffice:mous:index")

    context = {
        'title': 'Delete MoU',
        'document': document,
        'form': form
    }
    return render(request, 'mous/delete.html', context)


@login_required
def details(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(group=settings.GROUP_MOU), id=id
    )
    user = request.user
    if user.get_role_id() == settings.ROLE_USER_ID and \
       document.type == Document.TYPE.private:
        if not user.has_permission(id):
            messages.error(request, "You do not have an access, but you can request an access.")
            return redirect(reverse("backoffice:permission_requests:requests",
                                    args=[document.id, document.group]))

    if document.type == Document.TYPE.private:
        document.badge_type_class = "badge badge-danger p-1"
    else:
        document.badge_type_class = "badge badge-success p-1"

    if document.status == Document.STATUS.ongoing:
        document.badge_status_class = "badge badge-warning p-1"
    elif document.status == Document.STATUS.done:
        document.badge_status_class = "badge badge-success p-1"
    elif document.status == Document.STATUS.expired:
        document.badge_status_class = "badge badge-danger p-1"

    if document.is_active:
        document.record_status_class = "badge badge-success p-1 ml-1"
    else:
        document.record_status_class = "badge badge-danger p-1 ml-1"

    context = {
        'title': 'Details MoU',
        'document': document
    }
    return render(request, 'mous/details.html', context)


@legal_required
def upload(request, id):
    document = get_object_or_404(
        Document.objects.filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:mous:details", args=[document.id]))

    form = UploadForm(data=request.POST or None, files=request.FILES or None,
                      document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s files has already uploaded" %
                         (document.number))
        return redirect(reverse("backoffice:mous:details", args=[document.id]))

    context = {
        'title': 'Upload MoU',
        'document': document,
        'form': form
    }
    return render(request, 'mous/upload.html', context)


@legal_required
def change_status(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:mous:details", args=[document.id]))

    initial = {
        'status': document.status
    }

    form = ChangeStatusForm(data=request.POST or None, initial=initial,
                            document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s status has been changed into %s" %
                         (document.number, document.get_status_display().upper()))
        return redirect(reverse("backoffice:mous:details",
                        args=[document.id]))

    context = {
        'title': 'Change Status MoU',
        'form': form,
        'document': document
    }
    return render(request, 'mous/change_status.html', context)


@legal_required
def change_record_status(request, id):
    document = get_object_or_404(Document, id=id)

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:mous:details", args=[document.id]))

    form = ChangeRecordStatusForm(document=document, user=request.user)

    if form.is_valid():
        document = form.save()

        if document.is_active:
            string_status = "activated"
        else:
            string_status = "deactivated"

        messages.success(request, "Document # %s has been %s" % (document.number, string_status))
        return redirect("backoffice:mous:index")

    return redirect("backoffice:mous:index")


@login_required
def preview(request, id):
    document_file = get_object_or_404(DocumentFile, id=id)

    context = {
        'title': 'Preview MoU',
        'document_file': document_file
    }
    return render(request, 'mous/preview.html', context)


@legal_required
def remove(request, id):
    document_file = get_object_or_404(
        DocumentFile.objects.select_related('document', 'document__partner').filter(is_active=True), id=id
    )

    if document_file.document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document_file.document.number))
        return redirect(reverse("backoffice:mous:details", args=[document_file.document.id]))

    form = RemoveForm(data=request.POST or None, document_file=document_file, user=request.user)

    if form.is_valid():
        form.remove()
        messages.success(request, "MoU File of # %s has been deleted" % str(document_file.document.number))
        return redirect(reverse("backoffice:mous:details", args=[document_file.document.id]))
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Remove File MoU',
        'document_file': document_file,
        'form': form
    }
    return render(request, 'mous/remove.html', context)
