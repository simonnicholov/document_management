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
        'title': 'Detail Addendum'
    }
    return render(request, 'addendums/details.html', context)


def add(request, id):
    context = {
        'title': 'Add Addendum'
    }
    return render(request, 'addendums/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Addendum'
    }
    return render(request, 'addendums/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Addendum'
    }
    return render(request, 'addendums/delete.html', context)


def upload(request, id):
    context = {
        'title': 'Upload Addendum'
    }
    return render(request, 'addendums/upload.html', context)


def preview(request, id):
    context = {
        'title': 'Preview Addendum'
    }
    return render(request, 'addendums/preview.html', context)


def update_record_status(request, id):
    context = {
        'title': 'Update Record Status'
    }
    return render(request, 'addendums/update_record_status.html', context)
