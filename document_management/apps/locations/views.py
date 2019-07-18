from django.shortcuts import render


def index(request):
    context = {
        'title': 'Location'
    }
    return render(request, 'locations/index.html', context)


def add(request):
    context = {
        'title': 'Add Location'
    }
    return render(request, 'locations/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Location'
    }
    return render(request, 'locations/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Location'
    }
    return render(request, 'locations/delete.html', context)


def details(request, id):
    context = {
        'title': 'Details Location'
    }
    return render(request, 'locations/details.html', context)
