from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404

from document_management.apps.documents.models import Document
from document_management.apps.official_records.models import OfficialRecord
from document_management.core.decorators import legal_required

from .forms import UnrelatedOfficialRecordForm


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

    if request.user.get_role_id() == settings.ROLE_USER_ID and \
       document.type == Document.TYPE.private:
        messages.error(request, "You do not have an access, but you can request an access.")
        return redirect(reverse("backoffice:permission_requests:requests", args=[document.id, document.group]))

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
        'is_related': True
    }
    return render(request, 'official_records/unrelated/details.html', context)


@legal_required
def unrelated_add(request, id=None):
    form = UnrelatedOfficialRecordForm(data=request.POST or None, user=request.user)

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
    context = {
        'title': 'Unrelated Edit Official Records',
    }
    return render(request, 'official_records/unrelated/edit.html', context)


@legal_required
def unrelated_delete(request, id=None):
    context = {
        'title': 'Unrelated Delete Official Records',
    }
    return render(request, 'official_records/unrelated/delete.html', context)


@legal_required
def unrelated_upload(request, id=None):
    context = {
        'title': 'Unrelated Upload Official Records',
    }
    return render(request, 'official_records/unrelated/upload.html', context)


@legal_required
def unrelated_preview(request, id=None):
    context = {
        'title': 'Unrelated Preview Official Records',
    }
    return render(request, 'official_records/unrelated/preview.html', context)


@legal_required
def unrelated_change_status(request, id):
    context = {
        'title': 'Unrelated Change Status Official Records',
    }
    return render(request, 'official_records/unrelated/preview.html', context)


@legal_required
def unrelated_change_record_status(request, id=None):
    context = {
        'title': 'Unrelated Change Record Official Records',
    }
    return render(request, 'official_records/unrelated/add.html', context)


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
    return render(request, 'official_records/related.html', context)


@login_required
def related_lists(request, id):
    document = get_object_or_404(Document, id=id)
    official_records = document.official_records.order_by('-id')

    context = {
        'title': 'Search Official Records',
        'official_records': official_records,
        'document': document
    }
    return render(request, 'official_records/lists.html', context)
