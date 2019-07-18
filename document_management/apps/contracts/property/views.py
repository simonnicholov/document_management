from django.shortcuts import render

def index(request):
    context = {
        'title': 'Contract'
    }
    return render(request, 'contracts/property/index.html', context)

def add(request):
    context = {
        'title': 'Add Contract'
    }
    return render(request, 'contracts/property/add.html', context)

def edit(request, id):
    context = {
        'title': 'Edit Contract'
    }
    return render(request, 'contracts/property/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Contract'
    }
    return render(request, 'contracts/property/delete.html', context)


def details(request, id):
    context = {
        'title': 'Details Contract'
    }
    return render(request, 'contracts/property/details.html', context)


def upload(request, id):
    context = {
        'title': 'Upload Contract'
    }
    return render(request, 'contracts/property/upload.html', context)