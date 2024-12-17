from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from transactions.models import Transaction
from transactions.constants import TransactionType, TransactionCategory

def home(request):
    # Get current month's start and end dates
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if today.month == 12:
        month_end = today.replace(year=today.year + 1, month=1, day=1, hour=23, minute=59, second=59, microsecond=999999) - timezone.timedelta(days=1)
    else:
        month_end = today.replace(month=today.month + 1, day=1, hour=23, minute=59, second=59, microsecond=999999) - timezone.timedelta(days=1)

    # Get total income for current month
    total_income = Transaction.objects.filter(
        transaction_type=TransactionType.INCOME.value,
        date__range=(month_start, month_end)
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Calculate budget amounts based on total income
    budget_data = {
        TransactionCategory.NEEDS.value: {
            'budget': total_income * TransactionCategory.max_percentage(TransactionCategory.NEEDS.value) / 100,
            'spent': 0,
            'transactions': []
        },
        TransactionCategory.WANTS.value: {
            'budget': total_income * TransactionCategory.max_percentage(TransactionCategory.WANTS.value) / 100,
            'spent': 0,
            'transactions': []
        },
        TransactionCategory.SAVINGS.value: {
            'budget': total_income * TransactionCategory.max_percentage(TransactionCategory.SAVINGS.value) / 100,
            'spent': 0,
            'transactions': []
        }
    }

    # Get all expenses for current month
    expenses = Transaction.objects.filter(
        transaction_type=TransactionType.EXPENSE.value,
        date__range=(month_start, month_end)
    ).order_by('-date')

    # Calculate spent amounts and collect transactions for each category
    for expense in expenses:
        category_data = budget_data[expense.category]
        category_data['spent'] += expense.amount
        category_data['transactions'].append({
            'date': expense.date.strftime('%b %d'),
            'description': expense.description,
            'amount': expense.amount
        })

    # Get income transactions
    income_transactions = Transaction.objects.filter(
        transaction_type=TransactionType.INCOME.value,
        date__range=(month_start, month_end)
    ).order_by('-date')

    # Prepare context data
    context = {
        'total_income': total_income,
        'income': {
            'transactions': [{
                'date': t.date.strftime('%b %d'),
                'description': t.description,
                'amount': t.amount
            } for t in income_transactions]
        },
        TransactionCategory.NEEDS.value: budget_data[TransactionCategory.NEEDS.value],
        TransactionCategory.WANTS.value: budget_data[TransactionCategory.WANTS.value],
        TransactionCategory.SAVINGS.value: budget_data[TransactionCategory.SAVINGS.value]
    }

    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

# def contact(request):
#     return render(request, "core/contact.html")
