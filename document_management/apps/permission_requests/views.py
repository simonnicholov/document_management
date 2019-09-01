from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from document_management.apps.documents.models import Document
from document_management.apps.permission_requests.models import PermissionRequest
from document_management.core.decorators import user_required
from document_management.core.utils import prepare_datetime_range

from .forms import RequestPermissionForm


@user_required
def index(request):
    query = request.GET.get('query', '')
    request_date = request.GET.get('request_date', '')
    status = int(request.GET.get('status', 0))
    group = int(request.GET.get('group', 0))

    permission_requests = PermissionRequest.objects.select_related('document')

    if query:
        permission_requests = permission_requests.filter(Q(document__number__icontains=query) |
                                                         Q(document__subject__istartswith=query))

    if request_date:
        request_date = datetime.strptime(request_date, '%Y-%m-%d')
        start, end = prepare_datetime_range(request_date, request_date)
        permission_requests = permission_requests.filter(created__range=(start, end))

        request_date = request_date.strftime("%Y-%m-%d")

    if status > 0:
        permission_requests = permission_requests.filter(status=status)

    if group > 0:
        permission_requests = permission_requests.filter(document__group=group)

    permission_requests = permission_requests.order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(permission_requests, 25)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    for permission_request in page.object_list:
        if permission_request.status == PermissionRequest.STATUS.request:
            permission_request.badge_status_class = "badge badge-info p-1"
        elif permission_request.status == PermissionRequest.STATUS.approved:
            permission_request.badge_status_class = "badge badge-success p-1"
        else:
            permission_request.badge_status_class = "badge badge-danger p-1"

    context = {
        'title': 'List Requests',
        'document': Document,
        'permission_request': PermissionRequest,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'query': query,
        'group': group,
        'status': status,
        'request_date': request_date
    }
    return render(request, 'permission_requests/index.html', context)


@user_required
def requests(request, id, group):
    document = get_object_or_404(Document, id=id, group=group)

    if document.type == Document.TYPE.public:
        messages.error(request, "You do not have to request to view this document")
        return redirect("backoffice:documents:index")

    if not document.is_active:
        messages.error(request, "You can`t request to this document, because this document is inactive.")
        return redirect("backoffice:documents:index")

    if document.validate_request_permission(user=request.user):
        messages.error(request, "Please wait, you have already requested for this document.")
        return redirect("backoffice:permission_requests:index")

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

    form = RequestPermissionForm(data=request.POST or None, document=document,
                                 user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Your request has been submitted.")
        return redirect("backoffice:permission_requests:index")

    context = {
        'title': 'Request Permission',
        'document': document,
        'form': form
    }
    return render(request, 'permission_requests/requests.html', context)


@user_required
def details(request, id):
    permission_request = get_object_or_404(
        PermissionRequest.objects.select_related('document', 'user_action'), id=id)

    if permission_request.status == PermissionRequest.STATUS.request:
        permission_request.badge_status_class = "badge badge-info p-1"
    elif permission_request.status == PermissionRequest.STATUS.approved:
        permission_request.badge_status_class = "badge badge-success p-1"
    elif permission_request.status == PermissionRequest.STATUS.rejected:
        permission_request.badge_status_class = "badge badge-danger p-1"

    context = {
        'title': 'Details Permission',
        'permission_request': permission_request
    }
    return render(request, 'permission_requests/details.html', context)
