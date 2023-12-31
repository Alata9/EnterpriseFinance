# Generated by Django 4.2.2 on 2023-11-12 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Counterparties",
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
                ("counterparty", models.CharField(max_length=100, unique=True)),
                ("comments", models.CharField(blank=True, max_length=100, null=True)),
                ("suppliers", models.BooleanField(blank=True, default=False)),
                ("customer", models.BooleanField(blank=True, default=False)),
                ("employee", models.BooleanField(blank=True, default=False)),
                ("other", models.BooleanField(blank=True, default=False)),
            ],
            options={
                "verbose_name": "Counterparty",
                "verbose_name_plural": "Counterparties",
                "ordering": ["counterparty"],
            },
        ),
        migrations.CreateModel(
            name="Currencies",
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
                ("currency", models.CharField(max_length=10, unique=True)),
                ("code", models.CharField(max_length=3)),
            ],
            options={
                "verbose_name": "Currency",
                "verbose_name_plural": "Currencies",
                "ordering": ["currency"],
            },
        ),
        migrations.CreateModel(
            name="Items",
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
                ("item", models.CharField(max_length=100, unique=True)),
                (
                    "flow",
                    models.CharField(
                        blank=True,
                        choices=[("Receipts", "Receipts"), ("Payments", "Payments")],
                        max_length=10,
                    ),
                ),
                (
                    "group",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Sales_income", "Sales income"),
                            ("Direct_expenses", "Direct expenses"),
                            ("Administrative_expenses", "Administrative expenses"),
                            ("Commercial_expenses", "Commercial expenses"),
                            ("Production_costs", "Production costs"),
                            ("Other", "Other income and expenses"),
                            ("Loans", "Credits and loans"),
                            ("Fixed_assets", "Fixed assets"),
                            ("New_projects", "New projects"),
                        ],
                        max_length=100,
                    ),
                ),
            ],
            options={
                "verbose_name": "Item",
                "verbose_name_plural": "Items",
                "ordering": ["group", "item"],
            },
        ),
        migrations.CreateModel(
            name="Organization",
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
                ("organization", models.CharField(max_length=100, unique=True)),
                ("comments", models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={"ordering": ["organization"],},
        ),
        migrations.CreateModel(
            name="Project",
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
                ("project", models.CharField(max_length=100, unique=True)),
                ("comments", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
                "ordering": ["organization", "project"],
            },
        ),
        migrations.CreateModel(
            name="PaymentAccount",
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
                ("account", models.CharField(max_length=50, unique=True)),
                ("is_cash", models.BooleanField()),
                ("comments", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.currencies",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment account",
                "verbose_name_plural": "Payment accounts",
                "ordering": ["organization", "account"],
            },
        ),
        migrations.CreateModel(
            name="InitialDebts",
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
                    "debit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "credit",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                ("comments", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "type_debt",
                    models.CharField(
                        choices=[
                            ("", ""),
                            ("Lender", "Lender"),
                            ("Borrower", "Borrower"),
                            ("Other", "Other"),
                        ],
                        max_length=10,
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
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.currencies",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "Counterparty initial debts",
                "verbose_name_plural": "Counterparties initial debts",
                "ordering": ["counterparty", "organization"],
            },
        ),
        migrations.CreateModel(
            name="CurrenciesRates",
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
                (
                    "rate",
                    models.DecimalField(decimal_places=6, default=0.0, max_digits=15),
                ),
                (
                    "accounting_currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cur1",
                        to="directory.currencies",
                    ),
                ),
                (
                    "currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cur2",
                        to="directory.currencies",
                    ),
                ),
            ],
            options={
                "verbose_name": "Rate",
                "verbose_name_plural": "Currency rates",
                "ordering": ["date", "accounting_currency", "currency"],
            },
        ),
    ]
