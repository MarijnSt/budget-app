from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add/', views.TransactionCreateView.as_view(), name='add'),
] 