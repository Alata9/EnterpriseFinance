# Generated by Django 4.2.2 on 2023-06-25 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counterparties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counterparty', models.CharField(max_length=100, unique=True)),
                ('suppliers', models.BooleanField()),
                ('customer', models.BooleanField()),
                ('employee', models.BooleanField()),
                ('other', models.BooleanField()),
                ('comments', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Counterparty',
                'verbose_name_plural': 'Counterparties',
                'ordering': ['counterparty'],
            },
        ),
        migrations.CreateModel(
            name='Currencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=10, unique=True)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'ordering': ['currency'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.CharField(max_length=100)),
                ('comments', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'ordering': ['organization'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=100, unique=True)),
                ('comments', models.CharField(blank=True, max_length=250)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directory.organization')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['organization', 'project'],
            },
        ),
        migrations.CreateModel(
            name='PaymentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=50, unique=True)),
                ('is_cash', models.BooleanField()),
                ('comments', models.CharField(blank=True, max_length=100)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directory.currencies')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directory.organization')),
            ],
            options={
                'verbose_name': 'Payment account',
                'verbose_name_plural': 'Payment accounts',
                'ordering': ['organization', 'account'],
            },
        ),
    ]
