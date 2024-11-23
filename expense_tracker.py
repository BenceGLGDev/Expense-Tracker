import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup
DB_NAME = "data/expenses.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            date TEXT,
            category TEXT,
            amount REAL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(date, category, amount, note):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, note)
        VALUES (?, ?, ?, ?)
    ''', (date, category, amount, note))
    conn.commit()
    conn.close()
    print("Expense added successfully.")

def view_expenses(filter_category=None):
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM expenses"
    if filter_category:
        query += " WHERE category = ?"
        df = pd.read_sql_query(query, conn, params=(filter_category,))
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    print(df)
    return df

def export_data(filename, file_format="csv"):
    df = view_expenses()
    if file_format == "csv":
        df.to_csv(filename, index=False)
    elif file_format == "json":
        df.to_json(filename, orient="records")
    print(f"Data exported to {filename}")

def visualize_expenses():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT category, SUM(amount) as total FROM expenses GROUP BY category", conn)
    conn.close()

    if df.empty:
        print("No data to visualize.")
        return

    # Pie chart
    plt.pie(df["total"], labels=df["category"], autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.show()

def main():
    initialize_db()
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Export Data")
        print("4. Visualize Expenses")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            note = input("Enter note (optional): ")
            add_expense(date, category, amount, note)
        elif choice == "2":
            filter_category = input("Enter category to filter by (or press Enter for all): ")
            view_expenses(filter_category if filter_category else None)
        elif choice == "3":
            filename = input("Enter filename (e.g., expenses.csv): ")
            file_format = input("Enter format (csv/json): ").lower()
            export_data(filename, file_format)
        elif choice == "4":
            visualize_expenses()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
