# Generated by Django 5.1.5 on 2025-03-07 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herosection', '0005_alter_attendance_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstudent',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
