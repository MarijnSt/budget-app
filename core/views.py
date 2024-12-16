from django.shortcuts import render

def home(request):
    # This will later be calculated from actual transactions
    mock_data = {
        'total_income': 3000.00,
        'needs': {
            'budget': 1500.00,  # 50% of income
            'spent': 1070.00,   # under budget
            'transactions': [
                {'date': 'Mar 1', 'description': 'Rent', 'amount': 800.00},
                {'date': 'Mar 5', 'description': 'Groceries', 'amount': 150.00},
                {'date': 'Mar 10', 'description': 'Utilities', 'amount': 120.00},
            ]
        },
        'wants': {
            'budget': 900.00,   # 30% of income
            'spent': 1060.00,   # over budget
            'transactions': [
                {'date': 'Mar 3', 'description': 'Restaurant', 'amount': 45.00},
                {'date': 'Mar 8', 'description': 'Cinema', 'amount': 15.00},
                {'date': 'Mar 15', 'description': 'Shopping', 'amount': 1000.00},
            ]
        },
        'savings': {
            'budget': 600.00,   # 20% of income
            'spent': 600.00,    # exactly on budget
            'transactions': [
                {'date': 'Mar 1', 'description': 'Emergency Fund', 'amount': 400.00},
                {'date': 'Mar 1', 'description': 'Investment Account', 'amount': 200.00},
            ]
        }
    }
    return render(request, 'core/home.html', mock_data)

def about(request):
    return render(request, 'core/about.html')

# def contact(request):
#     return render(request, "core/contact.html")
