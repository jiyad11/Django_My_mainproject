# Generated by Django 4.2.1 on 2023-05-23 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('paid_by', models.CharField(max_length=100)),
                ('paid_date', models.DateField(null=True)),
                ('payment', models.CharField(max_length=100)),
                ('Customuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_no', models.CharField(max_length=30)),
                ('card_cvv', models.CharField(max_length=30)),
                ('expiry_month', models.CharField(max_length=20)),
                ('expiry_year', models.CharField(max_length=20)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fee_payment', to='myapp.bill')),
            ],
        ),
        migrations.RemoveField(
            model_name='user_payment',
            name='amount_and_bill',
        ),
        migrations.DeleteModel(
            name='payments',
        ),
        migrations.DeleteModel(
            name='user_payment',
        ),
    ]
