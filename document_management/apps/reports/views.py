from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

from document_management.core.decorators import legal_required

from .forms import ContractForm


@legal_required
def index(request):
    context = {
        'title': 'Reports'
    }
    return render(request, 'reports/index.html', context)


@legal_required
def contract(request):
    form = ContractForm(data=request.POST or None)

    if form.is_valid():
        response = form.generate_zip_response(HttpResponse(content_type='application/zip'))
        return response
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Report Contract',
        'form': form
    }
    return render(request, 'reports/contract.html', context)


@legal_required
def mou(request):
    context = {
        'title': 'Report MoU'
    }
    return render(request, 'reports/mou.html', context)


@legal_required
def official_record(request):
    context = {
        'title': 'Report Official Record'
    }
    return render(request, 'reports/official_record.html', context)


@legal_required
def company_regulations(request):
    context = {
        'title': 'Report Company Regulation'
    }
    return render(request, 'reports/company_regulations.html', context)
