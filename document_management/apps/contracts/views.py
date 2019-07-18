from django.shortcuts import render


def index(request):
    context = {
        'title': 'Contract'
    }
    return render(request, 'contracts/index.html', context)


def add(request):
    context = {
        'title': 'Add Contract'
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
