from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from document_management.apps.partners.models import Partner

from .forms import PartnerForm


def index(request):
    name = request.GET.get('name', '')
    director = request.GET.get('director', '')
    business_sector = int(request.GET.get('business_sector', 0))
    status = int(request.GET.get('status', -1))

    partners = Partner.objects.all()

    if name:
        partners = partners.filter(name__istartswith=name)

    if director:
        partners = partners.filter(director__istartswith=director)

    if business_sector > 0:
        partners = partners.filter(business_sector=business_sector)

    if status > -1:
        partners = partners.filter(is_active=bool(status))

    partners = partners.order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(partners, 25)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    for document in page.object_list:
        if document.is_active:
            document.badge_is_active_class = "badge badge-success p-1"
        else:
            document.badge_is_active_class = "badge badge-danger p-1"

    context = {
        'title': 'Partner',
        'partner': Partner,
        'page': page,
        'total_data': paginator.count,
        'total_pages': paginator.num_pages,
        'name': name,
        'director': director,
        'business_sector': business_sector,
        'status': status
    }
    return render(request, 'partners/index.html', context)


def add(request):
    form = PartnerForm(data=request.POST or None, user=request.user)

    if form.is_valid():
        partner = form.save()
        messages.success(request, f'{partner.name} has been added')
        return redirect('backoffice:partners:index')
    else:
        if form.has_error('__all__'):
            messages.error(request, form.non_field_errors()[0])

    context = {
        'title': 'Add Partner',
        'form': form
    }
    return render(request, 'partners/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Partner'
    }
    return render(request, 'partners/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Partner'
    }
    return render(request, 'partners/delete.html', context)


def details(request, id):
    partner = get_object_or_404(Partner, id=id)

    if partner.is_active:
        partner.record_status_class = "badge badge-success p-1 ml-1"
    else:
        partner.record_status_class = "badge badge-danger p-1 ml-1"

    context = {
        'title': 'Details Partner',
        'partner': partner
    }
    return render(request, 'partners/details.html', context)


def search(request):
    context = {
        'title': 'Search Partner'
    }
    return render(request, 'partners/search.html', context)


def change_record_status(request):
    context = {
        'title': 'Change Record Status'
    }
    return render(request, 'partners/search.html', context)
