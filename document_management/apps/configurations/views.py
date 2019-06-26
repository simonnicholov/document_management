from django.shortcuts import render


def category(request):
    context = {
        'title': 'Category Configurations'
    }
    return render(request, 'configurations/category.html', context)


def list(request, id):
    context = {
        'title': 'List Configurations'
    }
    return render(request, 'configurations/list.html', context)


def add(request, id):
    context = {
        'title': 'Add Configurations'
    }
    return render(request, 'configurations/add.html', context)


def edit(request, id):
    context = {
        'title': 'Edit Configurations'
    }
    return render(request, 'configurations/edit.html', context)


def delete(request, id):
    context = {
        'title': 'Delete Configurations'
    }
    return render(request, 'configurations/delete.html', context)
