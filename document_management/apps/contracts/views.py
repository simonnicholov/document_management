from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

from document_management.apps.documents.models import Document
from document_management.core.decorators import legal_required

from .forms import ContractForm


def index(request):
    query = request.GET.get('query', '')
    documents = Document.objects.select_related('partner').all()

    # employee = request.user.get_employee()
    # stores = employee.get_accessible_store_ids()
    # memberships = Membership.objects.select_related('user', 'user__profile')\
    #     .filter(creating_store__in=stores,
    #             merchant_group__id=settings.CMK_MERCHANT_GROUP_ID)

    # if query:
    #     try:
    #         query = normalize_phone(query)
    #     except phonenumbers.NumberParseException:
    #         messages.error(request, 'Please enter a valid mobile phone number')
    #         return redirect('frontdesk:members:index')

    #     memberships = memberships.filter(user__phone=query)

    page = request.GET.get('page', 1)

    paginator = Paginator(documents, 100)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'title': 'Contract',
        'page': page,
        'query': query
    }
    return render(request, 'contracts/index.html', context)


@legal_required
def add(request):
    form = ContractForm(data=request.POST or None)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        form.save()
        # messages.success(request, f'{product.name} has been added')
        return redirect('backoffice:contracts:index')

    context = {
        'title': 'Add Contract',
        'form': form
    }
    return render(request, 'contracts/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Contract'
    }
    return render(request, 'contracts/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Contract'
    }
    return render(request, 'contracts/delete.html', context)


def details(request, id):
    context = {
        'title': 'Details Contract'
    }
    return render(request, 'contracts/details.html', context)


def upload(request, id):
    context = {
        'title': 'Upload Contract'
    }
    return render(request, 'contracts/upload.html', context)


def change_status(request, id):
    context = {
        'title': 'Change Status'
    }
    return render(request, 'contracts/change_status.html', context)


def change_record_status(request, id):
    context = {
        'title': 'Change Status Contract'
    }
    return render(request, 'contracts/change_record_status.html', context)
