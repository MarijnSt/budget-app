from django.db import models

from .constants import TransactionCategory, TransactionType


class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TransactionType.choices())
    category = models.CharField(
        max_length=10,
        choices=TransactionCategory.choices(),
        null=True,
        blank=True,
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.transaction_type == TransactionType.EXPENSE.value and not self.category:
            raise ValidationError("Category is required for expenses")

        if self.transaction_type == TransactionType.INCOME.value and self.category:
            raise ValidationError("Category should not be set for income")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.description} - €{self.amount}"
