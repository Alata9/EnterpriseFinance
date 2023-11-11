# Generated by Django 4.2.2 on 2023-11-09 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0001_initial"),
        ("planning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="receiptsplan",
            name="calculation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="planning.calculations",
            ),
        ),
        migrations.AlterField(
            model_name="calculations",
            name="item",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="item1",
                to="directory.expensesitem",
            ),
        ),
    ]
