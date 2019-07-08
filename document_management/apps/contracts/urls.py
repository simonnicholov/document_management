from django.urls import path, include

app_name = 'contracts'

urlpatterns = [
    path('constructions/', include('document_management.apps.contracts.constructions.urls', namespace="constructions")),
]
