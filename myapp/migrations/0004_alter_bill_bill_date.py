# Generated by Django 4.2.1 on 2023-05-23 09:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_bill_paid_by_remove_bill_paid_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='bill_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]