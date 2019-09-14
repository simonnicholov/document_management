from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from document_management.apps.documents.models import Document, DocumentFile
from document_management.core.decorators import legal_required


@login_required
def index(request):
    query = request.GET.get('query', '')
    effective_date = request.GET.get('effective_date', '')
    category = int(request.GET.get('category', 0))

    documents = Document.objects.select_related('partner')\
        .filter(group=settings.GROUP_CONTRACT)


    if effective_date:
        effective_date = datetime.strptime(effective_date, '%Y-%m-%d').date()
        documents = documents.filter(effective_date=effective_date)
        effective_date = effective_date.strftime("%Y-%m-%d")

    if query:
        documents = documents.filter(Q(number__icontains=query) |
                                     Q(subject__icontains=query) |
                                     Q(partner__name__icontains=query))

    if category > 0:
        documents = documents.filter(category=category)

    documents = documents.order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(documents, 25)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Company Regulations',
        'document': Document,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'query': query,
        'category': category,
        'effective_date': effective_date
    }
    return render(request, 'company_regulations/index.html', context)


@legal_required
def add(request):
    context = {
        'title': 'Add Company Regulation',
    }
    return render(request, 'company_regulations/add.html', context)


@legal_required
def edit(request, id):
    context = {
        'title': 'Edit Company Regulation'
    }
    return render(request, 'company_regulations/edit.html', context)


@legal_required
def delete(request, id):
    context = {
        'title': 'Delete Company Regulation'
    }
    return render(request, 'company_regulations/delete.html', context)


@login_required
def details(request, id):
    context = {
        'title': 'Details Company Regulation'
    }
    return render(request, 'company_regulations/details.html', context)


@legal_required
def upload(request, id):
    context = {
        'title': 'Upload Company Regulation'
    }
    return render(request, 'company_regulations/details.html', context)


@legal_required
def change_status(request, id):
    context = {
        'title': 'Change Status Company Regulation'
    }
    return render(request, 'company_regulations/change_status.html', context)


@legal_required
def change_record_status(request, id):
    context = {
        'title': 'Change Record status Company Regulation'
    }
    return render(request, 'company_regulations/change_status.html', context)


@login_required
def preview(request, id):
    document_file = get_object_or_404(DocumentFile, id=id)

    context = {
        'title': 'Preview Contract',
        'document_file': document_file
    }
    return render(request, 'contracts/preview.html', context)
