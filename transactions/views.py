from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .constants import TransactionType
from .forms import TransactionForm
from .models import Transaction


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/transaction_form.html"
    success_url = reverse_lazy("core:home")

    def get_initial(self):
        initial = super().get_initial()
        transaction_type = self.request.GET.get("type")
        if transaction_type in [
            TransactionType.INCOME.value,
            TransactionType.EXPENSE.value,
        ]:
            initial["transaction_type"] = transaction_type
        return initial


class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/transaction_form.html"
    success_url = reverse_lazy("core:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context


class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = reverse_lazy("core:home")

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, "Transaction deleted successfully.")
            return response
        except Exception:
            messages.error(request, "Error deleting transaction.")
            return redirect("core:home")
