from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/', views.TransactionCreateView.as_view(), name='add'),
    path('edit/<int:pk>/', views.TransactionUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.TransactionDeleteView.as_view(), name='delete'),
] 