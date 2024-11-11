from django.db import migrations

def add_reservation_statuses(apps, schema_editor):
    ReservationStatuses = apps.get_model('loans', 'ReservationStatuses')
    statuses = ['Создана', 'Закрыта', 'Истекла', 'Отменена']

    for status_name in statuses:
        ReservationStatuses.objects.get_or_create(status_name=status_name)

class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_reservationstatuses'),
    ]

    operations = [
        migrations.RunPython(add_reservation_statuses),
    ]
