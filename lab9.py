from pymongo import MongoClient
from datetime import datetime

# Підключення до серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Створення або вибір бази даних
db = client['expense_manager']

# Створення колекції (аналог таблиці у MongoDB)
expenses_collection = db['expenses']

# CRUD операції
def create_expense(amount, category):
    expense_data = {
        'amount': amount,
        'category': category,
        'date': datetime.now()
    }
    result = expenses_collection.insert_one(expense_data)
    return result.inserted_id

def read_expenses():
    expenses = expenses_collection.find()
    return list(expenses)

def update_expense(expense_id, new_amount, new_category):
    query = {'_id': expense_id}
    update_data = {'$set': {'amount': new_amount, 'category': new_category}}
    result = expenses_collection.update_one(query, update_data)
    return result.modified_count > 0

def delete_expense(expense_id):
    query = {'_id': expense_id}
    result = expenses_collection.delete_one(query)
    return result.deleted_count > 0

# Приклад використання
expense_id_1 = create_expense(50, 'Food')
expense_id_2 = create_expense(30, 'Transportation')

expenses = read_expenses()
print("All Expenses:")
for expense in expenses:
    print(f"{expense['_id']} - {expense['amount']} in {expense['category']} on {expense['date']}")

update_expense(expense_id_1, 60, 'Dining Out')
expenses = read_expenses()
print("\nUpdated Expenses:")
for expense in expenses:
    print(f"{expense['_id']} - {expense['amount']} in {expense['category']} on {expense['date']}")

delete_expense(expense_id_2)
expenses = read_expenses()
print("\nExpenses after deletion:")
for expense in expenses:
    print(f"{expense['_id']} - {expense['amount']} in {expense['category']} on {expense['date']}")
