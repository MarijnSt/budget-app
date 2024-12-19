from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Transaction
from .constants import TransactionType, TransactionCategory

class TrasactionViewsTest(TestCase):
    def setUp(self):
        # Create a user (once auth is implemented)
        # self.user = User.objects.create_user(username='testuser', password='testpassword')
        # self.client.login(username='testuser', password='testpassword')

        # Create a sample transaction
        self.transaction = Transaction.objects.create(
            date = timezone.now(),
            description = 'Test Transaction',
            amount = 100.00,
            transaction_type = TransactionType.EXPENSE.value,
            category = TransactionCategory.NEEDS.value
        )

    def test_homepage_shows_sample_transaction(self):
        """
        When we visit the homepage, we should find the transaction that was created in the setUp function
        """
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Transaction')

    def test_transaction_create_view_with_type_param(self):
        """
        When we visit the transaction create view, the form should have initial data with the transaction type based on the query parameter
        """
        response = self.client.get(reverse('transactions:add') + '?type=income')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['transaction_type'], TransactionType.INCOME.value)
        
        response = self.client.get(reverse('transactions:add') + '?type=expense')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['transaction_type'], TransactionType.EXPENSE.value)
    
    def test_transaction_create_view_with_no_type_param(self):
        """
        When we visit the transaction create view, the form should not have any initial data if there is no type query parameter
        """
        response = self.client.get(reverse('transactions:add'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial, {})

    def test_transaction_create_view(self):
        """
        We're able to create a new transaction
        """
        # visit the page
        response = self.client.get(reverse('transactions:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transaction_form.html')

        # submit the form
        response = self.client.post(reverse('transactions:add'), {
            'date': timezone.now().date(),
            'description': 'Create Test Transaction',
            'amount': 100.00,
            'transaction_type': TransactionType.EXPENSE.value,
            'category': TransactionCategory.NEEDS.value
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(description='Create Test Transaction').exists())

    def test_transaction_create_view_with_invalid_data(self):
        """
        We should not be able to create a transaction with invalid data
        """
        response = self.client.post(reverse('transactions:add'), {
            'date': timezone.now().date(),
        })
        
        form = response.context['form']
        self.assertFalse(form.is_valid())

    def test_transaction_update_view(self):
        """
        We're able to update a transaction
        """
        response = self.client.get(reverse('transactions:edit', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/transaction_form.html')

        # update the transaction
        response = self.client.post(reverse('transactions:edit', args=[self.transaction.id]), {
            'date': timezone.now().date(),
            'description': 'Update Test Transaction',
            'amount': 200.00,
            'transaction_type': TransactionType.INCOME.value
        })

        self.assertEqual(response.status_code, 302)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.description, 'Update Test Transaction')
        self.assertEqual(self.transaction.amount, 200.00)
        self.assertEqual(self.transaction.transaction_type, TransactionType.INCOME.value)

    def test_transaction_delete_view(self):
        """
        We're able to delete a transaction
        """
        response = self.client.post(reverse('transactions:delete', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(id=self.transaction.id).exists())
