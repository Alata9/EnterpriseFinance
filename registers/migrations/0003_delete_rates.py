# Generated by Django 4.2.2 on 2023-09-02 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("registers", "0002_accountsettings_accounting_currency"),
    ]

    operations = [
        migrations.DeleteModel(name="Rates",),
    ]