# Generated by Django 2.0.4 on 2018-04-19 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_auto_20180419_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='usertobookrelations',
            options={'verbose_name': 'User-Book realations', 'verbose_name_plural': 'User-Book realations'},
        ),
        migrations.AlterField(
            model_name='usertobookrelations',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_book_relations', to='catalogue.Book'),
        ),
        migrations.AlterField(
            model_name='usertobookrelations',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_book_relations', to=settings.AUTH_USER_MODEL),
        ),
    ]
