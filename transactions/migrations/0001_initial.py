# Generated by Django 5.1.4 on 2024-12-17 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
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
                ("description", models.CharField(max_length=200)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("income", "Income"), ("expense", "Expense")],
                        max_length=7,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("needs", "Needs"),
                            ("wants", "Wants"),
                            ("savings", "Savings"),
                        ],
                        help_text="Category is required for expenses, leave empty for income",
                        max_length=10,
                        null=True,
                    ),
                ),
            ],
        ),
    ]