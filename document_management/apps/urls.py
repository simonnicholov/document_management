from django.urls import path, include

from . import views

app_name = 'apps'

urlpatterns = [
    # namespace urls
    path('', include('document_management.apps.users.urls', namespace="users")),
    path('addendum/', include('document_management.apps.addendums.urls', namespace="addendums")),
    path('event/', include('document_management.apps.events.urls', namespace="events")),
    path('location/', include('document_management.apps.locations.urls', namespace="locations")),
    path('partner/', include('document_management.apps.partners.urls', namespace="partners")),
    path('configuration/', include('document_management.apps.configurations.urls', namespace="configurations")),

    # documents urls
    path('contracts/', include('document_management.apps.contracts.urls', namespace="contracts")),

    # specific urls
    path('dashboard/', views.dashboard, name="dashboard"),
    path('permission-requests/', views.permission_requests, name="permission_requests"),
    path('approval-requests/', views.approval_requests, name="approval_requests"),
]
