# Generated by Django 4.1.5 on 2024-02-24 05:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('npi_number', models.CharField(max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Clinician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('specialization', models.CharField(max_length=100)),
                ('npi', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TotalLife_app.npi')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration_minutes', models.IntegerField()),
                ('reason_for_visit', models.TextField()),
                ('clinician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TotalLife_app.clinician')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TotalLife_app.patient')),
            ],
        ),
    ]
