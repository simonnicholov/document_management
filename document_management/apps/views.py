from django.shortcuts import render


def dashboard(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard.html', context)
