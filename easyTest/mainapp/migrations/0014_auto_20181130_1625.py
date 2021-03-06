# Generated by Django 2.1.2 on 2018-11-30 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0013_question_owner'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='student',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='student',
            name='group',
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(blank=True, default=3, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='tests',
            field=models.ManyToManyField(blank=True, related_name='groups', to='mainapp.Test'),
        ),
        migrations.AddField(
            model_name='student',
            name='in_groups',
            field=models.ManyToManyField(blank=True, related_name='students', to='mainapp.Group'),
        ),
        migrations.AddField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(blank=True, default=3, on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
