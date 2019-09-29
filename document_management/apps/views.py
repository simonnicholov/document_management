from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import Document
from document_management.apps.permission_requests.models import PermissionRequest
from document_management.core.decorators import legal_required, user_required

from .forms import PasswordChangeForm


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()

        if not user.role:
            messages.error(request, 'You do not have an access for this application !')
            return redirect('backoffice:login')

        login(request, user)

        if 'next' in request.POST:
            return redirect(request.POST.get('next'))
        else:
            role_id = user.get_role_id()
            if role_id == settings.ROLE_SUPERUSER_ID or \
               role_id == settings.ROLE_LEGAL_ID:
                return redirect('backoffice:dashboard_legal')
            return redirect('backoffice:dashboard_user')
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect("backoffice:login")


@legal_required
def dashboard_legal(request):
    document = Document.objects.filter(is_active=True)
    total_contract = document.filter(group=settings.GROUP_CONTRACT).count()
    total_mou = document.filter(group=settings.GROUP_MOU).count()
    total_official_record = document.filter(group=settings.GROUP_OFFICIAL_RECORD).count()
    total_company_regulation = document.filter(group=settings.GROUP_COMPANY_REGULATION).count()

    total_addendum = Addendum.objects.filter(is_active=True).count()
    total_approval = PermissionRequest.objects.all().count()

    today = datetime.now().date()
    next_month = today + relativedelta(months=+1)
    three_month = today + relativedelta(months=+3)

    # 3 months expiration
    three_month_lists = document.filter(expired_date__range=(today, three_month))

    # monthly expiration
    next_month_lists = document.filter(expired_date__range=(today, next_month))

    context = {
        'title': 'Dashboard',
        'total_contract': total_contract,
        'total_mou': total_mou,
        'total_official_record': total_official_record,
        'total_company_regulation': total_company_regulation,
        'total_addendum': total_addendum,
        'total_approval': total_approval,
        'total_three_months': three_month_lists.count(),
        'total_next_month': next_month_lists.count(),
        'three_month_lists': three_month_lists,
        'next_month_lists': next_month_lists
    }
    return render(request, 'dashboard_legal.html', context)


@user_required
def dashboard_user(request):
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'dashboard_user.html', context)


@login_required
def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your password has been successfully updated')
        # return redirect("backoffice:logout")

    context = {
        'form': form,
        'next': next,
        'title': 'Change Password',
    }
    return render(request, 'change_password.html', context)
