from django.shortcuts import render


def index(request):
    context = {
        'title': 'Events'
    }
    return render(request, 'events/index.html', context)


def select(request):
    context = {
        'title': 'Select Events'
    }
    return render(request, 'events/select.html', context)


def add(request):
    context = {
        'title': 'Add Events'
    }
    return render(request, 'events/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Events'
    }
    return render(request, 'events/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Events'
    }
    return render(request, 'events/delete.html', context)


def details(request, id):
    context = {
        'title': 'Details Events'
    }
    return render(request, 'events/details.html', context)
