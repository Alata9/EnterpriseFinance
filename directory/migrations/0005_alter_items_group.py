# Generated by Django 4.2.2 on 2023-11-21 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0004_alter_items_options_remove_items_item_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="items",
            name="group",
            field=models.CharField(
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
    ]