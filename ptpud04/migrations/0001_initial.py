# Generated by Django 5.0 on 2023-12-05 13:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MotoElectrica',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('tarifa_segundo', models.DecimalField(decimal_places=4, max_digits=6)),
            ],
            options={
                'verbose_name': 'Moto Electrica',
                'verbose_name_plural': 'Motos Electricas',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField()),
                ('fin', models.DateTimeField(blank=True, null=True)),
                ('tarifa_segundo', models.DecimalField(decimal_places=4, max_digits=6)),
                ('coste_total', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('moto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptpud04.motoelectrica')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ptpud04.usuario')),
            ],
            options={
                'verbose_name_plural': 'Alquileres',
            },
        ),
    ]
