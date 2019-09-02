from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from document_management.apps.documents.models import Document
from document_management.apps.permission_requests.models import PermissionRequest
from document_management.core.decorators import legal_required
from document_management.core.utils import prepare_datetime_range

from .forms import ApproveForm, RejectForm


@legal_required
def index(request):
    query = request.GET.get('query', '')
    request_date = request.GET.get('request_date', '')
    status = int(request.GET.get('status', 3))
    group = int(request.GET.get('group', 0))

    permission_requests = PermissionRequest.objects.select_related('document')

    if query:
        permission_requests = permission_requests.filter(Q(document__number__istartswith=query) |
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
        'title': 'Approval Requests',
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
    return render(request, 'approval_requests/index.html', context)


@legal_required
def approve(request, id):
    permission_request = get_object_or_404(
        PermissionRequest.objects.select_related('document'), id=id)

    if not permission_request.document.status:
        messages.error(request, "Document # %s status is inactive"
                       % (permission_request.document.number))
        return redirect("backoffice:approval_requests:index")

    if permission_request.status != PermissionRequest.STATUS.request:
        permission_request_status_display = permission_request.get_status_display().lower()
        messages.error(request, "Request # %s status has already %s"
                       % (permission_request.document.number, permission_request_status_display))
        return redirect("backoffice:approval_requests:index")

    form = ApproveForm(permission_request=permission_request, user=request.user)

    if form.is_valid():
        permission_request = form.save()
        messages.success(request, "Request # %s has been approved"
                         % (permission_request.document.number))
        return redirect("backoffice:approval_requests:index")

    return redirect("backoffice:approval_requests:index")


@legal_required
def reject(request, id):
    permission_request = get_object_or_404(
        PermissionRequest.objects.select_related('document'), id=id)

    if not permission_request.document.status:
        messages.error(request, "Document # %s status is inactive"
                       % (permission_request.document.number))
        return redirect("backoffice:approval_requests:index")

    if permission_request.status != PermissionRequest.STATUS.request:
        permission_request_status_display = permission_request.get_status_display().lower()
        messages.error(request, "Request # %s status has already %s"
                       % (permission_request.document.number, permission_request_status_display))
        return redirect("backoffice:approval_requests:index")

    form = RejectForm(data=request.POST or None, permission_request=permission_request,
                      user=request.user)

    if form.is_valid():
        permission_request = form.save()
        messages.success(request, "Request # %s has been rejected"
                         % (permission_request.document.number))
        return redirect("backoffice:approval_requests:index")
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Reject Requests',
        'form': form,
        'permission_request': permission_request
    }
    return render(request, 'approval_requests/reject.html', context)
