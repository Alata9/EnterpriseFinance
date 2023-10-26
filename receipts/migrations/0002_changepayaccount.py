# Generated by Django 4.2.2 on 2023-10-09 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0003_alter_initialdebts_type_debt"),
        ("receipts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChangePayAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.currencies",
                    ),
                ),
                (
                    "pay_account_from",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="account1",
                        to="directory.paymentaccount",
                    ),
                ),
                (
                    "pay_account_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="account2",
                        to="directory.paymentaccount",
                    ),
                ),
            ],
            options={
                "verbose_name": "Change payment account",
                "verbose_name_plural": "Changes payment account",
                "ordering": ["date", "pay_account_from", "pay_account_to"],
            },
        ),
    ]
