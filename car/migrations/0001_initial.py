# Generated by Django 4.2.7 on 2023-11-18 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('patent', models.CharField(max_length=8, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.CreateModel(
            name='CarRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enter_date', models.DateField(auto_now=True)),
                ('leave_date', models.DateField(null=True)),
                ('code', models.CharField(max_length=16, null=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='car.car')),
            ],
            options={
                'verbose_name': 'CarRegister',
                'verbose_name_plural': 'CarRegisters',
                'ordering': ('enter_date', 'leave_date'),
                'get_latest_by': ('enter_date', 'leave_date'),
            },
        ),
    ]