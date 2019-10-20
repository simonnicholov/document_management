from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404

from document_management.apps.documents.models import (Document, DocumentFile)
from document_management.apps.official_records.models import (OfficialRecord, OfficialRecordFile)
from document_management.core.decorators import legal_required

from .forms import (UnrelatedForm, UnrelatedDeleteForm,
                    UnrelatedChangeRecordStatusForm, UnrelatedChangeStatusForm,
                    UnrelatedUploadForm, UnrelatedRemoveForm)

from .forms import (RelatedForm, RelatedDeleteForm, RelatedUploadForm,
                    RelatedChangeRecordStatusForm, RelatedRemoveForm)


@login_required
def index(request):
    context = {
        'title': 'Official Records',
    }
    return render(request, 'official_records/index.html', context)


'''
 Region Unrelated
'''


@login_required
def unrelated(request):
    query = request.GET.get('query', '')
    category = int(request.GET.get('category', 0))
    type = int(request.GET.get('type', 0))
    status = int(request.GET.get('status', 0))

    documents = Document.objects.select_related('partner')\
        .filter(group=settings.GROUP_OFFICIAL_RECORD)

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
        'title': 'Unrelated Official Records',
        'official_record': OfficialRecord,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'query': query,
        'category': category,
        'type': type,
        'status': status
    }
    return render(request, 'official_records/unrelated/index.html', context)


@login_required
def unrelated_details(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(group=settings.GROUP_OFFICIAL_RECORD), id=id
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
        'title': 'Unrelated Details Official Records',
        'document': document,
        'is_related': False
    }
    return render(request, 'official_records/unrelated/details.html', context)


@legal_required
def unrelated_add(request, id=None):
    form = UnrelatedForm(data=request.POST or None, user=request.user)

    if form.is_valid():
        document = form.save()
        messages.success(request, f'{document.number} has been added')
        return redirect('backoffice:official_records:unrelated')
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Unrelated Add Official Records',
        'form': form
    }
    return render(request, 'official_records/unrelated/add.html', context)


@legal_required
def unrelated_edit(request, id=None):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document.id]))

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

    form = UnrelatedForm(data=request.POST or None,
                         initial=initial, user=request.user, is_update=True)

    if form.is_valid():
        form.save()
        messages.success(request, f'{document.number} has been updated')
        return redirect(reverse('backoffice:official_records:unrelated_details', args=[document.id]))

    context = {
        'title': 'Unrelated Edit Official Records',
        'document': document,
        'form': form
    }
    return render(request, 'official_records/unrelated/edit.html', context)


@legal_required
def unrelated_delete(request, id=None):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document.id]))

    if document.status == Document.STATUS.ongoing:
        document.badge_status_class = "badge badge-warning p-1"
    elif document.status == Document.STATUS.done:
        document.badge_status_class = "badge badge-success p-1"
    elif document.status == Document.STATUS.expired:
        document.badge_status_class = "badge badge-danger p-1"

    form = UnrelatedDeleteForm(data=request.POST or None, document=document,
                               user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s has been deleted" % document.number)
        return redirect("backoffice:official_records:unrelated")

    context = {
        'title': 'Unrelated Delete Official Records',
        'document': document,
        'form': form
    }
    return render(request, 'official_records/unrelated/delete.html', context)


@legal_required
def unrelated_upload(request, id=None):
    document = get_object_or_404(
        Document.objects.filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document.id]))

    form = UnrelatedUploadForm(data=request.POST or None, files=request.FILES or None,
                               document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s files has already uploaded" %
                         (document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document.id]))

    context = {
        'title': 'Unrelated Upload Official Records',
        'document': document,
        'form': form
    }
    return render(request, 'official_records/unrelated/upload.html', context)


@login_required
def unrelated_preview(request, id=None):
    document_file = get_object_or_404(DocumentFile, id=id)

    context = {
        'title': 'Unrelated Preview Official Records',
        'document_file': document_file
    }
    return render(request, 'official_records/unrelated/preview.html', context)


@legal_required
def unrelated_change_status(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document.id]))

    initial = {
        'status': document.status
    }

    form = UnrelatedChangeStatusForm(data=request.POST or None, initial=initial,
                                     document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s status has been changed into %s" %
                         (document.number, document.get_status_display().upper()))
        return redirect(reverse("backoffice:official_records:unrelated_details",
                        args=[document.id]))

    context = {
        'title': 'Unrelated Change Status Official Records',
        'form': form,
        'document': document
    }
    return render(request, 'official_records/unrelated/change_status.html', context)


@legal_required
def unrelated_change_record_status(request, id=None):
    document = get_object_or_404(Document, id=id)

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document.id]))

    form = UnrelatedChangeRecordStatusForm(document=document, user=request.user)

    if form.is_valid():
        document = form.save()

        if document.is_active:
            string_status = "activated"
        else:
            string_status = "deactivated"

        messages.success(request, "Document # %s has been %s" % (document.number, string_status))
        return redirect("backoffice:official_records:unrelated")

    return redirect("backoffice:official_records:unrelated")


@legal_required
def unrelated_remove(request, id):
    document_file = get_object_or_404(
        DocumentFile.objects.select_related('document', 'document__partner')
                            .filter(is_active=True), id=id
    )

    if document_file.document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (document_file.document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document_file.document.id]))

    form = UnrelatedRemoveForm(data=request.POST or None, document_file=document_file, user=request.user)

    if form.is_valid():
        form.remove()
        messages.success(request, "Official Record File of # %s has been deleted" % str(document_file.document.number))
        return redirect(reverse("backoffice:official_records:unrelated_details", args=[document_file.document.id]))
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Remove File Official Record',
        'document_file': document_file,
        'form': form
    }
    return render(request, 'official_records/unrelated/remove.html', context)


'''
 Region Related
'''


@login_required
def related(request):
    query = request.GET.get('query', '')
    category = int(request.GET.get('category', 0))
    group = int(request.GET.get('group', 0))
    signature_date = request.GET.get('signature_date', '')

    if query or category > 0 or group > 0 or signature_date:
        official_records = OfficialRecord.objects.select_related('document')

        if signature_date:
            signature_date = datetime.strptime(signature_date, '%Y-%m-%d').date()
            official_records = official_records.filter(signature_date=signature_date)
            signature_date = signature_date.strftime("%Y-%m-%d")

        if category > 0:
            official_records = official_records.filter(document__category=category)

        if group > 0:
            official_records = official_records.filter(document__group=group)

        if query:
            official_records = official_records.filter(Q(number__icontains=query) |
                                                       Q(subject__icontains=query))

        official_records = official_records.order_by('-id')
    else:
        official_records = []

    page = request.GET.get('page', 1)

    paginator = Paginator(official_records, 25)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Related Official Records',
        'official_record': OfficialRecord,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'query': query,
        'category': category,
        'group': group,
        'signature_date': signature_date
    }
    return render(request, 'official_records/related/index.html', context)


@login_required
def related_lists(request, id):
    document = get_object_or_404(Document, id=id)
    official_records = document.official_records.order_by('-id')

    context = {
        'title': 'Search Official Records',
        'official_records': official_records,
        'document': document
    }
    return render(request, 'official_records/related/lists.html', context)


@login_required
def related_details(request, id=None):
    official_record = get_object_or_404(
        OfficialRecord.objects.select_related('document'), id=id
    )

    user = request.user
    if user.get_role_id() == settings.ROLE_USER_ID and \
       official_record.document.type == Document.TYPE.private:
        if not user.has_permission(official_record.document.id):
            messages.error(request, "You do not have an access, but you can request an access to the document first.")
            return redirect(reverse("backoffice:permission_requests:requests",
                                    args=[official_record.document.id, official_record.document.group]))

    if official_record.is_active:
        official_record.record_status_class = "badge badge-success p-1 ml-1"
    else:
        official_record.record_status_class = "badge badge-danger p-1 ml-1"

    context = {
        'title': 'Related Details Official Records',
        'official_record': official_record,
        'document': official_record.document
    }
    return render(request, 'official_records/related/details.html', context)


@legal_required
def related_add(request, id=None):
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

    form = RelatedForm(data=request.POST or None, document=document,
                       user=request.user)

    if form.is_valid():
        official_record = form.save()
        messages.success(request, f'{official_record.number} has been added')
        return redirect(reverse('backoffice:official_records:related_lists', args=[document.id]))
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Related Add Official Records',
        'form': form,
        'document': document
    }
    return render(request, 'official_records/related/add.html', context)


@legal_required
def related_edit(request, id=None):
    official_record = get_object_or_404(
        OfficialRecord.objects.select_related('document')
                      .filter(is_active=True), id=id
    )

    if official_record.document.status == Document.STATUS.done:
        messages.error(request, "Official record can not be changed, the %s # %s status has already done"
                       % (official_record.document.get_group_display().lower(),
                          official_record.document.number))
        return redirect(reverse("backoffice:official_records:related_details",
                                args=[official_record.id]))

    if official_record.signature_date:
        signature_date = official_record.signature_date.strftime("%Y-%m-%d")
    else:
        signature_date = ''

    if official_record.effective_date:
        effective_date = official_record.effective_date.strftime("%Y-%m-%d")
    else:
        effective_date = ''

    initial = {
        'number': official_record.number,
        'subject': official_record.subject,
        'signature_date': signature_date,
        'effective_date': effective_date,
        'description': official_record.description,
        'amount': official_record.amount,
        'job_specification': official_record.job_specification,
        'retention_period': official_record.retention_period
    }

    form = RelatedForm(data=request.POST or None, initial=initial,
                       document=official_record.document, user=request.user, is_update=True)

    if form.is_valid():
        form.save()
        messages.success(request, f'{official_record.number} has been updated')
        return redirect(reverse('backoffice:official_records:related_details',
                                args=[official_record.id]))
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Related Edit Official Records',
        'official_record': official_record,
        'document': official_record.document,
        'form': form
    }
    return render(request, 'official_records/related/edit.html', context)


@legal_required
def related_delete(request, id=None):
    official_record = get_object_or_404(
        OfficialRecord.objects.select_related('document')
                              .filter(is_active=True), id=id
    )

    if official_record.document.status == Document.STATUS.done:
        messages.error(request, "Official record can not be deleted, the %s # %s status has already done"
                       % (official_record.document.get_group_display().lower(),
                          official_record.document.number))
        return redirect(reverse("backoffice:official_records:related_details",
                                args=[official_record.id]))

    form = RelatedDeleteForm(data=request.POST or None,
                             official_record=official_record,
                             user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Official record # %s has been deleted" % official_record.number)
        return redirect(reverse("backoffice:official_records:related_lists",
                                args=[official_record.document.id]))

    context = {
        'title': 'Related Delete Official Records',
        'official_record': official_record,
        'form': form
    }
    return render(request, 'official_records/related/delete.html', context)


@legal_required
def related_upload(request, id=None):
    official_record = get_object_or_404(
        OfficialRecord.objects.select_related('document')
                      .filter(is_active=True), id=id
    )

    if official_record.document.status == Document.STATUS.done:
        messages.error(request, "Official record can not be uploaded, the %s # %s status has already done"
                       % (official_record.document.get_group_display().lower(),
                          official_record.document.number))
        return redirect(reverse("backoffice:official_records:related_details",
                                args=[official_record.id]))

    form = RelatedUploadForm(data=request.POST or None, files=request.FILES or None,
                             official_record=official_record, user=request.user)

    if form.is_valid():
        official_record = form.save()
        messages.success(request, "Official record # %s files has already uploaded" %
                         (official_record.number))
        return redirect(reverse("backoffice:official_records:related_details",
                                args=[official_record.id]))

    context = {
        'title': 'Related Upload Official Records',
        'official_record': official_record,
        'form': form
    }
    return render(request, 'official_records/related/upload.html', context)


@login_required
def related_preview(request, id=None):
    official_record_file = get_object_or_404(OfficialRecordFile, id=id)

    context = {
        'title': 'Related Preview Official Records',
        'official_record_file': official_record_file
    }
    return render(request, 'official_records/related/preview.html', context)


@legal_required
def related_change_record_status(request, id=None):
    official_record = get_object_or_404(OfficialRecord.objects.select_related('document'), id=id)

    if official_record.document.status == Document.STATUS.done:
        messages.error(request, "Official record can not be changed, the %s # %s status has already done"
                       % (official_record.document.get_group_display().lower(),
                          official_record.document.number))
        return redirect(reverse("backoffice:official_records:related_details",
                                args=[official_record.id]))

    form = RelatedChangeRecordStatusForm(official_record=official_record, user=request.user)

    if form.is_valid():
        official_record = form.save()

        if official_record.is_active:
            string_status = "activated"
        else:
            string_status = "deactivated"

        messages.success(request, "Official record # %s has been %s" % (official_record.number, string_status))
        return redirect(reverse("backoffice:official_records:related_lists",
                                args=[official_record.document.id]))

    return redirect(reverse("backoffice:official_records:related_lists",
                            args=[official_record.document.id]))


@legal_required
def related_remove(request, id):
    official_record_file = get_object_or_404(
        OfficialRecordFile.objects.select_related('official_record', 'official_record__document',
                                                  'official_record__document__partner')
                                  .filter(is_active=True), id=id
    )

    official_record = official_record_file.official_record

    if official_record.document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has already done" % (official_record.document.number))
        return redirect(reverse("backoffice:official_records:related_details", args=[official_record.document.id]))

    form = RelatedRemoveForm(data=request.POST or None, official_record_file=official_record_file,
                             user=request.user)

    if form.is_valid():
        form.remove()
        messages.success(request, "Official Record File of # %s has been deleted"
                                  % str(official_record.document.number))
        return redirect(reverse("backoffice:official_records:related_details", args=[official_record.document.id]))
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Remove File Contract',
        'official_record_file': official_record_file,
        'form': form
    }
    return render(request, 'official_records/related/remove.html', context)
