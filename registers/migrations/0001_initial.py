# Generated by Django 4.2.2 on 2023-09-12 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("directory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AccountSettings",
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
                    "multiple_organizations",
                    models.BooleanField(
                        verbose_name="Keep records of multiple organizations"
                    ),
                ),
                (
                    "multiple_accounts",
                    models.BooleanField(verbose_name="Use multiple payment accounts"),
                ),
                (
                    "multiple_currencies",
                    models.BooleanField(
                        verbose_name="Use multiple accounting currencies"
                    ),
                ),
                (
                    "multiple_projects",
                    models.BooleanField(verbose_name="Keep records of projects"),
                ),
                (
                    "accounting_currency",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="directory.currencies",
                    ),
                ),
                (
                    "organization_default",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="directory.organization",
                    ),
                ),
            ],
        ),
    ]