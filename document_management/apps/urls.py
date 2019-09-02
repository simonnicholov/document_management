from django.urls import path, include

from . import views

app_name = 'backoffice'

urlpatterns = [
    # namespace urls
    path('users/', include('document_management.apps.users.urls', namespace="users")),
    path('addendum/', include('document_management.apps.addendums.urls', namespace="addendums")),
    path('event/', include('document_management.apps.events.urls', namespace="events")),
    path('location/', include('document_management.apps.locations.urls', namespace="locations")),
    path('partner/', include('document_management.apps.partners.urls', namespace="partners")),
    path('configuration/', include('document_management.apps.configurations.urls', namespace="configurations")),
    path('permission-requests/', include('document_management.apps.permission_requests.urls'),
         name="permission_requests"),
    path('approval-requests/', include('document_management.apps.approval_requests.urls'),
         name="approval_requests"),

    # documents urls
    path('contracts/', include('document_management.apps.contracts.urls', namespace="contracts")),

    # specific urls
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    path('dashboard/legal', views.dashboard_legal, name="dashboard_legal"),
    path('dashboard/user', views.dashboard_user, name="dashboard_user"),
    path('change-password/', views.change_password, name="change_password"),
]
