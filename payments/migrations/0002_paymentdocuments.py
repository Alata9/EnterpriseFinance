# Generated by Django 4.2.2 on 2023-11-11 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0003_alter_items_flow_alter_items_group_alter_items_item"),
        ("planning", "0004_alter_calculations_flow"),
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentDocuments",
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
                (
                    "flow",
                    models.CharField(
                        blank=True,
                        choices=[("Receipts", "Receipts"), ("Payments", "Payments")],
                        max_length=10,
                    ),
                ),
                ("date", models.DateField()),
                (
                    "inflow_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "outflow_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                ("comments", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.paymentaccount",
                    ),
                ),
                (
                    "by_request",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="planning.paymentsplan",
                    ),
                ),
                (
                    "counterparty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.counterparties",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.currencies",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.items",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.organization",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment document",
                "verbose_name_plural": "Payment documents",
                "ordering": ["flow", "organization", "date", "item"],
            },
        ),
    ]