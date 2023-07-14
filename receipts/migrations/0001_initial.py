# Generated by Django 4.2.2 on 2023-06-25 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('directory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_group', models.CharField(max_length=50)),
                ('comments', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Income group',
                'verbose_name_plural': 'Income groups',
                'ordering': ['income_group'],
            },
        ),
        migrations.CreateModel(
            name='IncomeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income_item', models.CharField(max_length=50)),
                ('income_group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='receipts.incomegroup')),
            ],
            options={
                'verbose_name': 'Income item',
                'verbose_name_plural': 'Income items',
                'ordering': ['income_group', 'income_item'],
            },
        ),
        migrations.CreateModel(
            name='ReceiptsPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('is_cash', models.BooleanField(default=False, null=True)),
                ('comments', models.CharField(blank=True, max_length=255)),
                ('counterparty', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='directory.counterparties')),
                ('currency', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='directory.currencies')),
                ('item', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='receipts.incomeitem')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directory.organization')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='directory.project')),
            ],
            options={
                'verbose_name': 'Receipt plan',
                'verbose_name_plural': 'Receipts plan',
                'ordering': ['organization', 'date', 'item'],
            },
        ),
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('comments', models.CharField(blank=True, max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directory.paymentaccount')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directory.counterparties')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directory.currencies')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='receipts.incomeitem')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='directory.organization')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='directory.project')),
            ],
            options={
                'verbose_name': 'Receipt',
                'verbose_name_plural': 'Receipts',
                'ordering': ['organization', 'date', 'item'],
            },
        ),
    ]
