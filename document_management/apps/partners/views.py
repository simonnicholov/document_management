from django.shortcuts import render


def index(request):
    context = {
        'title': 'Partner'
    }
    return render(request, 'partners/index.html', context)


def add(request):
    context = {
        'title': 'Add Partner'
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
    context = {
        'title': 'Details Partner'
    }
    return render(request, 'partners/details.html', context)
