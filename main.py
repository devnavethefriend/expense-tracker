import sqlite3
import datetime

# Create database connection
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

# Initialize database table
cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        date Date,
        name TEXT,
        category TEXT,
        amount REAL
    )
""")

# Function to add a new expense to the database
def add_expense(date, name, amount, category):
    cur.execute('INSERT INTO expenses (date, name, category, amount) VALUES (?, ?, ?, ?)', (date, name, category, amount))
    conn.commit()

# Function to show a summary of the expenses
def show_summary():
    cur.execute('SELECT SUM(amount) FROM expenses')
    total_expenses = cur.fetchone()[0]
    print(f'Total Expenses: ${total_expenses:.2f}')

    cur.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    category_summary = cur.fetchall()
    print('Category Summary:')
    for category, total in category_summary:
        print(f'{category}: ${total:.2f}')

# Function to prompt the user for a category
def get_category():
    cur.execute('SELECT DISTINCT category FROM expenses')
    categories = [row[0] for row in cur.fetchall()]
    print('Existing Categories:')
    for index, category in enumerate(categories):
        print(f'{index + 1}. {category}')
    while True:
        category = input('> Pick category or create a new one: ').strip()
        if category.isnumeric() and int(category) in range(1, len(categories) + 1):
            return categories[int(category) - 1]
        else:
            category_name = category.strip()
            cur.execute('INSERT INTO expenses (category) VALUES (?)', (category_name,))
            conn.commit()
            print(f'New category "{category_name}" created successfully!')
            return category_name

# Function to delete expenses
def clear_expense():
    cur.execute('DELETE FROM expenses')
    conn.commit()
    print('Cleared successfully!')

# Main loop to prompt the user for input
while True:
    print('> Enter a command:')
    print('1. Add expense')
    print('2. Show summary')
    print('3. Delete')
    print('4. Quit')

    command = input('> ')

    if command == '1':
        date = input('> Enter the date (YYYY-MM-DD): ')
        name = input('> Enter expense name: ')
        amount = float(input('> Enter expense amount: '))
        category = get_category()
        add_expense(date, name, amount, category)
        print('Expense added successfully!')

    elif command == '2':
        show_summary()

    elif command == '3':
        clear_expense()

    elif command == '4':
        break

    else:
        print('Invalid command. Please try again.')

# Close the database connection
conn.close()
