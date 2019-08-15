from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from document_management.apps.documents.models import Document
from document_management.core.decorators import legal_required

from .forms import ContractForm, DeleteForm


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
    context = {
        'title': 'Edit Contract'
    }
    return render(request, 'contracts/edit.html', context)


@legal_required
def delete(request, id):
    document = get_object_or_404(
        Document.objects.select_related('partner', 'location')
                .filter(is_active=True), id=id
    )

    form = DeleteForm(data=request.POST or None, document=document, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Document # { document.number } has been delete")
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
    context = {
        'title': 'Change Status'
    }
    return render(request, 'contracts/change_status.html', context)


@legal_required
def change_record_status(request, id):
    context = {
        'title': 'Change Status Contract'
    }
    return render(request, 'contracts/change_record_status.html', context)
