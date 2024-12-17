from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Transaction
from .forms import TransactionForm
from .constants import TransactionType

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('core:home')

    def get_initial(self):
        initial = super().get_initial()
        transaction_type = self.request.GET.get('type')
        if transaction_type in [TransactionType.INCOME.value, TransactionType.EXPENSE.value]:
            initial['transaction_type'] = transaction_type
        return initial
