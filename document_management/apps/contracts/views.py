from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, reverse, get_object_or_404

from document_management.apps.documents.models import Document
from document_management.core.decorators import legal_required

from .forms import (ContractForm, DeleteForm, ChangeRecordStatusForm,
                    ChangeStatusForm)


@login_required
def index(request):
    query = request.GET.get('query', '')
    category = int(request.GET.get('category', 0))
    type = int(request.GET.get('type', 0))
    status = int(request.GET.get('status', 0))

    documents = Document.objects.select_related('partner')

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
            document.badge_type = "badge badge-danger p-1"
        else:
            document.badge_type = "badge badge-success p-1"

        if document.status == Document.STATUS.ongoing:
            document.badge_status = "badge badge-warning p-1"
        elif document.status == Document.STATUS.done:
            document.badge_status = "badge badge-success p-1"
        else:
            document.badge_status = "badge badge-danger p-1"

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
    return render(request, 'contracts/index.html', context)


@legal_required
def add(request):
    form = ContractForm(data=request.POST or None)

    if form.is_valid():
        document = form.save()
        messages.success(request, f'{document.number} has been added')
        return redirect('backoffice:contracts:index')
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Add Contract',
        'form': form
    }
    return render(request, 'contracts/add.html', context)


@legal_required
def edit(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    initial = {
        'number': document.number,
        'subject': document.subject,
        'effective_date': document.effective_date,
        'expired_date': document.expired_date,
        'location': document.location,
        'category': document.category,
        'type': document.type,
        'description': document.description,
        'partner': document.partner,
        'amount': document.amount,
        'job_specification': document.job_specification,
        'beginning_period': document.beginning_period,
        'ending_period': document.ending_period,
        'retention_period': document.retention_period
    }

    form = ContractForm(data=request.POST or None, initial=initial)

    print(form)
    if form.is_valid():
        form.save()
        return redirect(reverse('backoffice:contracts:index', args=[document.id]))

    context = {
        'title': 'Edit Contract',
        'document': document,
        'form': form
    }
    return render(request, 'contracts/edit.html', context)


@legal_required
def delete(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has been done" % (document.number))
        return redirect(reverse("backoffice:contracts:details", args=[document.id]))

    form = DeleteForm(data=request.POST or None, document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s has been deleted" % document.number)
        return redirect("backoffice:contracts:index")

    context = {
        'title': 'Delete Contract',
        'document': document,
        'form': form
    }
    return render(request, 'contracts/delete.html', context)


@login_required
def details(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location'), id=id
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

    context = {
        'title': 'Details Contract',
        'document': document
    }
    return render(request, 'contracts/details.html', context)


@legal_required
def upload(request, id):
    context = {
        'title': 'Upload Contract'
    }
    return render(request, 'contracts/upload.html', context)


@legal_required
def change_status(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner')
                .filter(is_active=True), id=id
    )

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has been done" % (document.number))
        return redirect(reverse("backoffice:contracts:details", args=[document.id]))

    initial = {
        'status': document.status
    }

    form = ChangeStatusForm(data=request.POST or None, initial=initial,
                            document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # %s status has been changed into %s" %
                         (document.number, document.get_status_display().upper()))
        return redirect(reverse("backoffice:contracts:details",
                        args=[document.id]))

    context = {
        'title': 'Change Status',
        'form': form,
        'document': document
    }
    return render(request, 'contracts/change_status.html', context)


@legal_required
def change_record_status(request, id):
    document = get_object_or_404(Document, id=id)

    if document.status == Document.STATUS.done:
        messages.error(request, "Document # %s status has been done" % (document.number))
        return redirect(reverse("backoffice:contracts:details", args=[document.id]))

    form = ChangeRecordStatusForm(document=document, user=request.user)

    if form.is_valid():
        document = form.save()

        if document.is_active:
            string_status = "activated"
        else:
            string_status = "deactivated"

        messages.success(request, "Document # %s has been %s" % (document.number, string_status))
        return redirect("backoffice:contracts:index")

    return redirect("backoffice:contracts:index")
