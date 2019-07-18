from django.shortcuts import render


def index(request):
    context = {
        'title': 'Search Addendums'
    }
    return render(request, 'addendums/index.html', context)


def lists(request, id):
    context = {
        'title': 'List Addendums'
    }
    return render(request, 'addendums/lists.html', context)


def details(request, id):
    context = {
        'title': 'Detail Addendums'
    }
    return render(request, 'addendums/details.html', context)


def add(request, id):
    context = {
        'title': 'Add Addendums'
    }
    return render(request, 'addendums/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Addendums'
    }
    return render(request, 'addendums/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Addendums'
    }
    return render(request, 'addendums/delete.html', context)


def upload(request, id):
    context = {
        'title': 'Upload Addendums'
    }
    return render(request, 'addendums/upload.html', context)


def preview(request, id):
    context = {
        'title': 'Preview Addendums'
    }
    return render(request, 'addendums/preview.html', context)
