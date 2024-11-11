import django.db.models.deletion
from django.db import migrations, models

def create_statuses(apps, schema_editor):
    CopiesStatus = apps.get_model('books', 'CopiesStatus')
    statuses = ['Доступна', 'Выдана', 'Забронирована', 'Утеряна', 'В ремонте']
    for status in statuses:
        CopiesStatus.objects.get_or_create(status=status)

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_booksauthors_book_authors_booksgenres_book_genres'),
    ]

    operations = [
        migrations.CreateModel(
            name='CopiesStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='book_covers/'),
        ),
        migrations.AlterField(
            model_name='bookcopy',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.copiesstatus'),
        ),
        migrations.RunPython(create_statuses),
    ]
