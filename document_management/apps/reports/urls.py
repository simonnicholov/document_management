from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.index, name="index"),

    path('contract/', views.contract, name="contract"),
    path('mou/', views.mou, name="mou"),
    path('official-record/', views.official_record, name="official_record"),
    path('company-reguations/', views.company_regulations, name="company_regulations"),
]
