# Generated by Django 4.2.1 on 2023-06-08 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_appointment_date_remove_appointment_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='type_of_work',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.work_types'),
        ),
    ]
