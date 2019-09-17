from django_extensions.management.base import LoggingBaseCommand

from document_management.apps.addendums.models import Addendum
from document_management.apps.documents.models import Document
from document_management.apps.locations.models import Location
from document_management.apps.official_records.models import OfficialRecord
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

        location1 = Location.objects.get(id=1)
        location2 = Location.objects.get(id=2)
        location3 = Location.objects.get(id=3)

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

        partner1 = Partner.objects.get(id=1)
        partner2 = Partner.objects.get(id=2)
        partner3 = Partner.objects.get(id=3)
        partner4 = Partner.objects.get(id=4)

        # create document
        Document.objects.bulk_create([

            # contract
            Document(partner=partner1, location=location1, number='CONTRACT-001',
                     subject='CONTRACT-001 Subject', signature_date='2019-09-18',
                     effective_date='2019-09-19', expired_date='2019-09-30', amount=50000000,
                     group=Document.GROUP.contract, category=Document.CATEGORY.construction,
                     type=Document.TYPE.private, job_specification='Pembuatan keramik',
                     retention_period=90),
            Document(partner=partner2, location=location2, number='CONTRACT-002',
                     subject='CONTRACT-002 Subject', signature_date='2019-09-19',
                     effective_date='2019-09-20', expired_date='2019-10-1', amount=75000000,
                     group=Document.GROUP.contract, category=Document.CATEGORY.property,
                     type=Document.TYPE.public, job_specification='Pembuatan bata',
                     retention_period=45),
            Document(partner=partner3, location=location3, number='CONTRACT-003',
                     subject='CONTRACT-003 Subject', signature_date='2019-09-19',
                     effective_date='2019-09-22', expired_date='2019-10-3', amount=35500000,
                     group=Document.GROUP.contract, category=Document.CATEGORY.other,
                     type=Document.TYPE.private, job_specification='Pembuatan dinding kayu',
                     retention_period=75),

            # mou
            Document(partner=partner4, location=location3, number='MOU-001',
                     subject='MOU-001 Subject', signature_date='2019-09-15',
                     effective_date='2019-09-17', expired_date='2019-09-25', amount=50000000,
                     group=Document.GROUP.mou, category=Document.CATEGORY.construction,
                     type=Document.TYPE.private, job_specification='Pemasangan alumunium',
                     retention_period=120),
            Document(partner=partner2, location=location2, number='MOU-002',
                     subject='MOU-002 Subject', signature_date='2019-09-19',
                     effective_date='2019-09-23', expired_date='2019-10-1', amount=75000000,
                     group=Document.GROUP.mou, category=Document.CATEGORY.property,
                     type=Document.TYPE.public, job_specification='Pembuatan bata',
                     retention_period=45),
            Document(partner=partner3, location=location1, number='MOU-003',
                     subject='MOU-003 Subject', signature_date='2019-09-17',
                     effective_date='2019-09-25', expired_date='2019-09-27', amount=35500000,
                     group=Document.GROUP.mou, category=Document.CATEGORY.other,
                     type=Document.TYPE.private, job_specification='Pembuatan pipa pvc',
                     retention_period=25),


            # official record
            Document(partner=partner1, location=location3, number='OFFICIAL-RECORD-001',
                     subject='OFFICIAL-RECORD-001 Subject', signature_date='2019-09-15',
                     effective_date='2019-09-17', expired_date='2019-09-25', amount=50000000,
                     group=Document.GROUP.official_record, category=Document.CATEGORY.construction,
                     type=Document.TYPE.private, job_specification='Pemasangan alumunium',
                     retention_period=120),
            Document(partner=partner3, location=location2, number='OFFICIAL-RECORD-002',
                     subject='OFFICIAL-RECORD-002 Subject', signature_date='2019-09-14',
                     effective_date='2019-09-15', expired_date='2019-09-25', amount=25500000,
                     group=Document.GROUP.official_record, category=Document.CATEGORY.property,
                     type=Document.TYPE.public, job_specification='Pembuatan batako',
                     retention_period=37),
            Document(partner=partner2, location=location1, number='OFFICIAL-RECORD-003',
                     subject='OFFICIAL-RECORD-003 Subject', signature_date='2019-09-12',
                     effective_date='2019-09-13', expired_date='2019-09-20', amount=32500000,
                     group=Document.GROUP.official_record, category=Document.CATEGORY.other,
                     type=Document.TYPE.private, job_specification='Pembuatan besi plamir',
                     retention_period=15),

            # company regulation
            Document(number='COMPANY-REGULATION-001', subject='COMPANY-REGULATION-001 Subject',
                     effective_date='2019-09-17', group=Document.GROUP.company_regulation,
                     type=Document.TYPE.public,
                     category=Document.CATEGORY.director_decisions),
            Document(number='COMPANY-REGULATION-002', subject='COMPANY-REGULATION-002 Subject',
                     effective_date='2019-09-18', group=Document.GROUP.company_regulation,
                     type=Document.TYPE.public,
                     category=Document.CATEGORY.circular_letter),
            Document(number='COMPANY-REGULATION-003', subject='COMPANY-REGULATION-003 Subject',
                     effective_date='2019-09-19', group=Document.GROUP.company_regulation,
                     type=Document.TYPE.public,
                     category=Document.CATEGORY.other),

        ])

        document1 = Document.objects.get(id=21)
        document2 = Document.objects.get(id=22)

        document4 = Document.objects.get(id=24)
        document5 = Document.objects.get(id=25)

        document7 = Document.objects.get(id=27)
        document8 = Document.objects.get(id=28)

        Addendum.objects.bulk_create([

            # addendum contract
            Addendum(document=document1, number='CONTRACT-001-ADDENDUM-001',
                     subject='CONTRACT-001-ADDENDUM-001 Subject', signature_date='2019-09-20',
                     effective_date='2019-09-20', expired_date='2019-09-30',
                     amount=78500000, job_specification='Buat addendum contract 001-1',
                     retention_period=80),
            Addendum(document=document1, number='CONTRACT-001-ADDENDUM-002',
                     subject='CONTRACT-001-ADDENDUM-002 Subject', signature_date='2019-09-21',
                     effective_date='2019-09-22', expired_date='2019-09-30',
                     amount=32350000, job_specification='Buat addendum contract 001-2',
                     retention_period=35),
            Addendum(document=document2, number='CONTRACT-002-ADDENDUM-001',
                     subject='CONTRACT-002-ADDENDUM-001 Subject', signature_date='2019-09-21',
                     effective_date='2019-09-21', expired_date='2019-09-30',
                     amount=99250000, job_specification='Buat addendum contract 002-1',
                     retention_period=90),

            # addendum mou
            Addendum(document=document4, number='MOU-001-ADDENDUM-001',
                     subject='MOU-001-ADDENDUM-001 Subject', signature_date='2019-09-20',
                     effective_date='2019-09-20', expired_date='2019-09-25',
                     amount=78500000, job_specification='Buat addendum mou 001',
                     retention_period=80),
            Addendum(document=document5, number='MOU-002-ADDENDUM-001',
                     subject='MOU-002-ADDENDUM-001 Subject', signature_date='2019-09-19',
                     effective_date='2019-09-23', expired_date='2019-10-1',
                     amount=83750000, job_specification='Buat addendum mou 002-1',
                     retention_period=95),
            Addendum(document=document5, number='MOU-002-ADDENDUM-002',
                     subject='MOU-002-ADDENDUM-002 Subject', signature_date='2019-09-20',
                     effective_date='2019-09-24', expired_date='2019-10-1',
                     amount=17750000, job_specification='Buat addendum mou 002-2',
                     retention_period=65),
            Addendum(document=document5, number='MOU-002-ADDENDUM-003',
                     subject='MOU-002-ADDENDUM-003 Subject', signature_date='2019-09-21',
                     effective_date='2019-09-25', expired_date='2019-10-1',
                     amount=23750000, job_specification='Buat addendum mou 002-3',
                     retention_period=73),
        ])

        OfficialRecord.objects.bulk_create([

            # official record contract
            OfficialRecord(document=document1, number='CONTRACT-001-OFFICIAL-RECORD-001',
                           subject='CONTRACT-001-OFFICIAL-RECORD-001 Subject', signature_date='2019-09-20',
                           effective_date='2019-09-20', expired_date='2019-09-30',
                           amount=78500000, job_specification='Buat official record contract 001-1',
                           retention_period=80),
            OfficialRecord(document=document1, number='CONTRACT-001-OFFICIAL-RECORD-002',
                           subject='CONTRACT-001-OFFICIAL-RECORD-002 Subject', signature_date='2019-09-21',
                           effective_date='2019-09-22', expired_date='2019-09-30',
                           amount=32350000, job_specification='Buat official record contract 001-2',
                           retention_period=35),
            OfficialRecord(document=document2, number='CONTRACT-002-OFFICIAL-RECORD-001',
                           subject='CONTRACT-002-OFFICIAL-RECORD-001 Subject', signature_date='2019-09-21',
                           effective_date='2019-09-21', expired_date='2019-09-30',
                           amount=99250000, job_specification='Buat official record contract 002-1',
                           retention_period=90),

            # official record mou
            OfficialRecord(document=document4, number='MOU-001-OFFICIAL-RECORD-001',
                           subject='MOU-001-OFFICIAL-RECORD-001 Subject', signature_date='2019-09-20',
                           effective_date='2019-09-20', expired_date='2019-09-25',
                           amount=78500000, job_specification='Buat official record mou 001',
                           retention_period=80),
            OfficialRecord(document=document5, number='MOU-002-OFFICIAL-RECORD-001',
                           subject='MOU-002-OFFICIAL-RECORD-001 Subject', signature_date='2019-09-19',
                           effective_date='2019-09-23', expired_date='2019-10-1',
                           amount=83750000, job_specification='Buat official record mou 002-1',
                           retention_period=95),
            OfficialRecord(document=document5, number='MOU-002-OFFICIAL-RECORD-002',
                           subject='MOU-002-OFFICIAL-RECORD-002 Subject', signature_date='2019-09-20',
                           effective_date='2019-09-24', expired_date='2019-10-1',
                           amount=17750000, job_specification='Buat official record mou 002-2',
                           retention_period=65),
            OfficialRecord(document=document5, number='MOU-002-OFFICIAL-RECORD-003',
                           subject='MOU-002-OFFICIAL-RECORD-003 Subject', signature_date='2019-09-21',
                           effective_date='2019-09-25', expired_date='2019-10-1',
                           amount=23750000, job_specification='Buat official record mou 002-3',
                           retention_period=73),
        ])
