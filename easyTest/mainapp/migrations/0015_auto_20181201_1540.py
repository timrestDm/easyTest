# Generated by Django 2.1.2 on 2018-12-01 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20181130_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='related_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
