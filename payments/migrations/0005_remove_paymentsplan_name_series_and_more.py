# Generated by Django 4.2.2 on 2023-10-27 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0004_calculations_frequency_calculations_loan_rate"),
    ]

    operations = [
        migrations.RemoveField(model_name="paymentsplan", name="name_series",),
        migrations.AddField(
            model_name="paymentsplan",
            name="calculation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="payments.calculations",
            ),
        ),
    ]
