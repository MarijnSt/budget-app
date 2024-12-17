from enum import Enum

class TransactionType(Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

    @classmethod
    def choices(cls):
        return [(type.value, type.name.title()) for type in cls]

class TransactionCategory(Enum):
    NEEDS = 'needs'
    WANTS = 'wants'
    SAVINGS = 'savings'

    @classmethod
    def choices(cls):
        return [(category.value, category.name.title()) for category in cls]
    
    @classmethod
    def max_percentage(cls, category):
        percentages = {
            cls.NEEDS.value: 50,
            cls.WANTS.value: 30,
            cls.SAVINGS.value: 20
        }
        return percentages.get(category, 0) 