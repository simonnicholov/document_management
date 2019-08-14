from django_extensions.management.base import LoggingBaseCommand

from document_management.apps.locations.models import Location
from document_management.apps.role_permissions.models import Role, Permission, RolePermission
from document_management.apps.partners.models import Partner


class Command(LoggingBaseCommand):

    def handle(self, *args, **options):
        # create location
        Location.objects.bulk_create([
            Location(code='BDG', name='Bandung'),
            Location(code='JKT', name='Jakarta'),
            Location(code='TGR', name='Tangerang'),
        ])

        # create role
        Role.objects.bulk_create([
            Role(name='Superuser'),
            Role(name='Legal'),
            Role(name='User'),
        ])

        # create permission
        Permission.objects.bulk_create([
            Permission(name='Insert'),
            Permission(name='Update'),
            Permission(name='Delete'),
            Permission(name='View'),
            Permission(name='Approve'),
            Permission(name='Upload'),
            Permission(name='Download'),
        ])

        # create role permission
        role_superuser = Role.objects.get(id=1)
        role_legal = Role.objects.get(id=2)
        role_user = Role.objects.get(id=3)

        permission_insert = Permission.objects.get(id=1)
        permission_update = Permission.objects.get(id=2)
        permission_delete = Permission.objects.get(id=3)
        permission_view = Permission.objects.get(id=4)
        permission_approve = Permission.objects.get(id=5)
        permission_upload = Permission.objects.get(id=6)
        permission_download = Permission.objects.get(id=7)

        RolePermission.objects.bulk_create([
            RolePermission(role=role_superuser, permission=permission_insert),
            RolePermission(role=role_superuser, permission=permission_update),
            RolePermission(role=role_superuser, permission=permission_delete),
            RolePermission(role=role_superuser, permission=permission_view),
            RolePermission(role=role_superuser, permission=permission_approve),
            RolePermission(role=role_superuser, permission=permission_upload),
            RolePermission(role=role_superuser, permission=permission_download),

            RolePermission(role=role_legal, permission=permission_insert),
            RolePermission(role=role_legal, permission=permission_update),
            RolePermission(role=role_legal, permission=permission_delete),
            RolePermission(role=role_legal, permission=permission_view),
            RolePermission(role=role_legal, permission=permission_approve),
            RolePermission(role=role_legal, permission=permission_upload),
            RolePermission(role=role_legal, permission=permission_download),

            RolePermission(role=role_user, permission=permission_view),
        ])

        # create partner
        Partner.objects.bulk_create([
            Partner(name='PT Sukses Abadi Jaya', director='Owen Khong'),
            Partner(name='PT Selalu Maju Sejahtera', director='Bradon Lim'),
            Partner(name='PT Maju Tanpa Henti', director='Michael Ng'),
            Partner(name='PT Melaju Kencang', director='Nadiem Oct'),
        ])
