# A personal finance app. 

import sqlite3

# Create the database file.
f_db = sqlite3.connect("expenditure.db")

# Get cursor.
cursor = f_db.cursor() 

# Create the tables and fields.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS spending_categories (id INTEGER PRIMARY KEY UNIQUE, 
               expense_categories TEXT UNIQUE)
""")
f_db.commit()  # Commit transaction.

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (expense_id INTEGER PRIMARY KEY, expense_amount DECIMAL,
               expense_type TEXT, transaction_description TEXT, FOREIGN KEY(expense_type) 
               REFERENCES expense_categories(id)) 
""")
f_db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS earnings_categories (income_id INTEGER PRIMARY KEY UNIQUE, 
               income_categories TEXT UNIQUE)
""")
f_db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (earnings_id INTEGER PRIMARY KEY, income_amount DECIMAL,
               income_type TEXT, income_description TEXT, FOREIGN KEY(income_type)
               REFERENCES income_categories(income_id))
""")
f_db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (budget_id TEXT UNIQUE, budget_amount DECIMAL,
               FOREIGN KEY(budget_id) REFERENCES expense_categories(id))
""")
f_db.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_goals (goal_id INTEGER UNIQUE PRIMARY KEY, 
               savings_goal DECIMAL)
               
""")
f_db.commit()

# Add records. 'or ignore' stops an error when the program runs again.
cursor.execute("""
INSERT OR IGNORE INTO spending_categories VALUES
        (1, "Supermarket")
""")
f_db.commit()
 
cursor.execute("""
    INSERT OR IGNORE INTO expenses VALUES
        (1000, 47.31, 1, "Food")    
""")
f_db.commit()

cursor.execute("""
    INSERT OR IGNORE INTO earnings_categories VALUES
        (100, "wages")    
""")
f_db.commit()

cursor.execute("""
    INSERT OR IGNORE INTO income VALUES
        ("5000", 2500, 100, "Monthly Wages")    
""")
f_db.commit()

cursor.execute("""
    INSERT OR IGNORE INTO financial_goals VALUES
        (1, 700)    
""")
f_db.commit()

while True:
    menu_options = input("""\nSelect an option:
        1 - Create an expense category
        2 - Add expense
        3 - Delete expense
        4 - View expenses
        5 - View expenses by category
        6 - View expense categories
        7 - Delete an expense category
        8 - Create an income category
        9 - Add income
        10 - Delete income
        11 - View income and see current balance
        12 - View income by category
        13 - View income categories
        14 - Delete an income category
        15 - Set budget for an expense category 
        16 - View budgets
        17 - Set financial goal
        18 - View progress toward financial goal
        19 - Exit
        """)
    if menu_options == "1":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            new_expense_category = input("Enter a name for this spending category: ")
            expense_category_id = int(input("Create a numerical ID for this category: "))
            if len(str(expense_category_id)) < 3:  # Restrict expense ID to two digits.
                cursor.execute("""
                INSERT INTO spending_categories(expense_categories, id)
                VALUES (?, ?)
                """, (new_expense_category, expense_category_id))
                f_db.commit()
                f_db.close()
                print("\nThis new category is ready to start tracking!")
            else:
                print("\nThe ID should only be 2 digits.")
        except ValueError as e:
            print("\nThe ID must be a number")
        except sqlite3.IntegrityError as e:
            print("\nThat already exists!")

    elif menu_options == "2":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM spending_categories""")
            expense_id = cursor.fetchall()  # Create a variable to verify category ID. 
            id_check = []  # Create a list to store ID's.
            for rows in expense_id:
                id = rows[0]
                id_check.append(id)  # Add ID's to the list.
            purchase_type = int(input("What kind of purchase was it? Enter the ID: "))
            if purchase_type in id_check:
                amount_spent = float(input("How much did you spend?: "))
                expense_description = input("Enter a description: ")
                cursor.execute("""
                INSERT INTO expenses(expense_amount, expense_type, transaction_description)
                VALUES (?, ?, ?)
                """, (amount_spent, purchase_type, expense_description))
                f_db.commit()
                f_db.close()
                print("\nExpense added!")
            else:
                print("\nYou don't have this category. Create a new tracking category first.")
        except ValueError as e:
            print("\nEnter a valid number only.")
    
    elif menu_options == "3":  # Enable user to remove an expense.
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM expenses""")
            expense_row = cursor.fetchall()
            f_db.commit()
            print(f"All expenses: {expense_row}")  # Includes an identifier for deletion.
            expense_check = []
            for rows in expense_row:
                row_id = rows[0]
                expense_check.append(row_id)
            expense_to_remove = int(input("\nEnter the four digit ID:  "))
            if expense_to_remove in expense_check:
                cursor.execute("""DELETE FROM expenses WHERE expense_id = ?
                """, (expense_to_remove,))
                f_db.commit()
                f_db.close()
                print("\nThe expense has been removed!")
            else:
                print("\nInvalid ID. It's the 4 digit number to the left of the expense.")
        except ValueError as e:
            f_db.rollback()  # Revert back to the state before the error.
            print("\nThe expense could not be removed.")

    elif menu_options == "4":
        f_db = sqlite3.connect("expenditure.db")
        cursor = f_db.cursor()
        cursor.execute("""SELECT SUM(expense_amount) FROM expenses""")
        for total_spending in cursor.fetchall():
            expenses = total_spending[0]  # Capture the figure outside a list or tuple.
        f_db.commit()
        print(f"\nYou have spent £{expenses} in total.")
        cursor.execute("""SELECT expense_amount, expense_type, transaction_description
                        FROM expenses""")
        list_of_expenditure = cursor.fetchall()
        print(f"\nList of expenditure: {list_of_expenditure}\n")
        f_db.close()
        # Not including current balance here enhances usability of the app.
        # Some users may only want to track expenses without including income.

    elif menu_options == "5":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            ask_user_which_expense = int(input("Which category? Enter the ID number: "))
            cursor.execute("""SELECT SUM(expense_amount) FROM expenses 
                           WHERE expense_type = ?""", (ask_user_which_expense,))
            for expenses_by_category in cursor.fetchall():
                category_expenses = expenses_by_category[0]
            print(f"\nTotal expenditure in this category: £{category_expenses} ")
            f_db.commit()
            cursor.execute("""SELECT expense_type, expense_amount, transaction_description 
                           FROM expenses WHERE expense_type = ?""", (ask_user_which_expense,))
            expenses_in_category = cursor.fetchall()
            print(f"\nExpenses in this category: {expenses_in_category}\n")
            f_db.close()
        except ValueError as e:
            print("\nThe ID must be a valid integer that you registered.")

    elif menu_options == "6":  # Enable user to check which categories they have.
        f_db = sqlite3.connect("expenditure.db")
        cursor = f_db.cursor()
        cursor.execute("""SELECT * FROM spending_categories""")
        user_expense_categories = cursor.fetchall()
        f_db.commit()
        f_db.close()
        print(f"\nExpense categories: {user_expense_categories}")

    elif menu_options == "7":  # Enable user to remove expense categories.
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM spending_categories""")
            category_list = cursor.fetchall()
            f_db.commit()
            print(f"Expense category list: {category_list}\n")
            category_check = []
            for rows in category_list:
                category_id = rows[0]
                category_check.append(category_id)
            category_to_delete = int(input("Enter an ID to remove a category: "))
            if category_to_delete in category_check:
                cursor.execute("""DELETE FROM spending_categories 
                               WHERE id = ?""", (category_to_delete,))
                f_db.commit()
                f_db.close()
                print("\nThis spending category has been successfully removed!")
            else:
                print("\nThat is not a valid spending category ID!")
        except ValueError as e:
            print("\nThe ID is the number of a category you registered!")
    
    elif menu_options == "8":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            income_category_id = int(input("Create an ID with more than 2-digits: "))
            # For clarity, restrict income ID to require more digits than the expense ID.
            if len(str(income_category_id)) > 2:
                new_income_category = input("Enter a name for this income category: ")
                cursor.execute("""
                INSERT INTO earnings_categories(income_id, income_categories)
                VALUES (?, ?)
                """, (income_category_id, new_income_category))
                f_db.commit()
                f_db.close()
                print("\nThis new category is ready to start tracking!")
            else:
                print("\nThe income ID number should have at least 3 digits.")
        except ValueError as e:
            print("\nThe ID should be 3 or more numbers only.")
        except sqlite3.IntegrityError as e:
            print("\nThat already exists!")

    elif menu_options == "9":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM earnings_categories""")
            earnings_id = cursor.fetchall()
            id_check = []
            for rows in earnings_id:
                id = rows[0]
                id_check.append(id)
            income_source = int(input("What income source was it? Enter the ID: "))
            if income_source in id_check:
                amount_earned = float(input("How much did you earn?: "))
                describe_income = input("Enter a description: ")
                cursor.execute("""
                INSERT INTO income(income_amount, income_type, income_description)
                VALUES (?, ?, ?)
                """, (amount_earned, income_source, describe_income))
                f_db.commit()
                f_db.close()
                print("\nIncome added!")
            else:
                print("\nYou don't have this category. Create a new tracking category first.")
        except ValueError as e:
            print("\nThat is not a valid ID category")

    elif menu_options == "10":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM income""")
            income_row = cursor.fetchall()
            f_db.commit()
            print(f"All income: {income_row}")  # Include a unique identifier for deletion.
            income_check = []
            for rows in income_row:
                row_id = rows[0]
                income_check.append(row_id)
            income_to_remove = int(input("\nEnter the four digit ID (first number):  "))
            if income_to_remove in income_check:
                cursor.execute("""DELETE FROM income WHERE earnings_id = ?
                """, (income_to_remove,))
                f_db.commit()
                f_db.close()
                print("\nThis specific income has been removed!")
            else:
                print("\nInvalid ID. It's the first number starting with '5'.")
        except ValueError as e:
            f_db.rollback()
            print("\nThe amount could not be updated.")

    elif menu_options == "11":
        f_db = sqlite3.connect("expenditure.db")
        cursor = f_db.cursor()
        cursor.execute("""SELECT SUM(income_amount) FROM income""")
        for total_income in cursor.fetchall():
            income = total_income[0]
        f_db.commit()
        print(f"\nYour total income earned is £{income}.")
        cursor.execute("""SELECT SUM(income_amount) FROM income""")
        for income in cursor.fetchall():
            total_income = income[0]
        f_db.commit()
        cursor.execute("""SELECT SUM(expense_amount) FROM expenses""")
        for spending in cursor.fetchall():
            spending = spending[0]
        f_db.commit()
        print(f"\nYour current balance is £{total_income - spending:.2f}.")
        cursor.execute("""SELECT income_amount, income_type, income_description
                        FROM income""")
        list_of_income = cursor.fetchall()
        f_db.commit()
        print(f"\nList of income: {list_of_income}")
        f_db.close()

    elif menu_options == "12":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            ask_user_which_income_type = int(input("Which category? Enter the ID:  "))
            cursor.execute("""SELECT SUM(income_amount) FROM income WHERE income_type = ?
                           """, (ask_user_which_income_type,))
            for income_by_category in cursor.fetchall():
                income_acquired = income_by_category[0]
            print(f"\nAmount earned in this category: £{income_acquired} ")
            f_db.commit()
            cursor.execute("""SELECT income_type, income_amount, income_description 
                           FROM income WHERE income_type = ?""", (ask_user_which_income_type,))
            income_from_category = cursor.fetchall()
            print(f"\nDetails: {income_from_category}")
            f_db.close()
        except ValueError as e:
            print("\nThe ID must be the one that you registered for this category")

    elif menu_options == "13":
        f_db = sqlite3.connect("expenditure.db")
        cursor = f_db.cursor()
        cursor.execute("""SELECT * FROM earnings_categories""")
        user_income_categories = cursor.fetchall()
        f_db.commit()
        f_db.close()
        print(f"\nIncome categories: {user_income_categories}")
    
    elif menu_options == "14":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM earnings_categories""")
            income_category_list = cursor.fetchall()
            f_db.commit()
            print(f"\nIncome category list: {income_category_list}\n")
            category_check = []
            for rows in income_category_list:
                category_id = rows[0]
                category_check.append(category_id)
            category_to_delete = int(input("Enter ID to remove a category: "))
            if category_to_delete in category_check:
                cursor.execute("""DELETE FROM earnings_categories 
                               WHERE income_id = ?""", (category_to_delete,))
                f_db.commit()
                f_db.close()
                print("\nThis income category has been successfully removed!")
            else:
                print("\nThat is not a valid spending category ID!")
        except ValueError as e:
            print("\nIt should be the numerical ID that you registered.")

    elif menu_options == "15":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM spending_categories""")
            expense_categories = cursor.fetchall()
            f_db.commit()
            category_check = []
            for rows in expense_categories:
                expense_category_id = rows[0]
                category_check.append(expense_category_id)
            budget_id = int(input("Enter an expense category ID to set a budget: "))
            if budget_id in category_check:
                budget_category = float(input("Enter the budget you're setting: "))
                cursor.execute("""
                INSERT INTO budgets(budget_id, budget_amount) 
                VALUES (?, ?)  
                """, (budget_id, budget_category,))
                f_db.commit()
                f_db.close()
                print("\nThis budget has been set!")
        except ValueError as e:
            print("\nGo to menu option '6' to check which expense categories you have.")
        except sqlite3.IntegrityError as e:
            print("\nYou have already set a budget for this category.")
        # Once set, don't permit the user to change a budget. 
        # This stops user from continually increasing the budget and overspending.

    elif menu_options == "16":
        f_db = sqlite3.connect("expenditure.db")
        cursor = f_db.cursor()
        cursor.execute("""SELECT * FROM budgets""")
        budget_categories = cursor.fetchall()
        f_db.commit()
        budget_category_check = []
        for rows in budget_categories:
            budget_category_id = rows[0]
            budget_category_check.append(budget_category_id)
        budget_id = input("Enter an expense category ID to see the budget for it: ")
        if budget_id in budget_category_check:
            cursor.execute("""SELECT budget_amount FROM budgets""")
            for budgets in cursor.fetchall():
                category_budget = budgets[0]
            print(f"\nBudget for this category: £{category_budget}.")
            f_db.commit()
            cursor.execute("""SELECT SUM(expense_amount) FROM expenses
                           WHERE expense_type = ?""", (budget_id,))
            for category_expenses in cursor.fetchall():
                expenses_in_category = category_expenses[0]
            print(f"\nYou have spent: £{expenses_in_category}.")
            f_db.commit()
            f_db.close()
        else:
            print("\nOnly enter the ID for a budget you already set.")
    
    elif menu_options == "17":
        try:
            f_db = sqlite3.connect("expenditure.db")
            cursor = f_db.cursor()
            cursor.execute("""SELECT * FROM financial_goals""")
            financial_goals_list = cursor.fetchall()
            f_db.commit()
            goals_id_check = []
            for rows in financial_goals_list:
                goals_id = rows[0]
                goals_id_check.append(goals_id)
                proceed_to_financial_goal = int(input("Enter '1' to set a financial goal: "))
            if proceed_to_financial_goal in goals_id_check:
                saving_goal = float(input("How much money do you want to have?: "))
                cursor.execute("""UPDATE financial_goals SET savings_goal = ?
                            WHERE goal_id = ?""", (saving_goal, proceed_to_financial_goal))
                f_db.commit()
                f_db.close()
                # Only permit user to set one goal at a time.
                # A new goal can be set at any time, however.
                # This stops data discrepancies i.e. if user adds conflicting goals.
                print("\nYour financial goal has been added!")
        except ValueError as e:
                print("\nEnter the integer '1' to proceed to set a goal.")
                print("\nThen when prompted enter a figure only i.e. '50000'.")

    elif menu_options == "18":
        f_db = sqlite3.connect("expenditure.db")
        cursor = f_db.cursor()
        # Query the database and store required data in separate variables.
        cursor.execute("""SELECT SUM(expense_amount) FROM expenses""")
        for spending in cursor.fetchall():
            spending = spending[0]
        f_db.commit()
        cursor.execute("""SELECT savings_goal FROM financial_goals WHERE goal_id = 1""")
        for rows in cursor.fetchall():
            goals = rows[0]
        f_db.commit()
        cursor.execute("""SELECT SUM(income_amount) FROM income""")
        for income in cursor.fetchall():
            total_income = income[0]
        f_db.commit()
        current_funds = total_income - spending  # Store user's current funds.
        if current_funds < goals:  # Notify user about the progress of their goal. 
            print(f"\nYou need £{goals - current_funds:.2f} to reach your goal.")
            print(f"\nYour target is £{goals}.")
        else:
            print("\nYou have already reached your goal!")
            print(f"\nYour goal was to reach £{goals}.") 
        print(f"\nYou currently have £{total_income - spending:.2f}.")
        f_db.close()
        
    elif menu_options == "19":
        print("\nExiting the app....")
        break
        
    else:
        print("\ninvalid input!")

    f_db.close() # Close the database connection.
