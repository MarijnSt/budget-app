from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "description", "amount", "transaction_type", "category"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required by default
        for field in self.fields.values():
            field.required = True
        # Make category optional (will be validated in model)
        self.fields["category"].required = False
