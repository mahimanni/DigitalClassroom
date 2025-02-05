# Generated by Django 5.1.5 on 2025-02-05 09:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herosection', '0004_alter_staffs_address_alter_subjects_course_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
