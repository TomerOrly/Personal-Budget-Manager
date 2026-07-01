from datetime import datetime
from models import Transaction
from budget_manager import BudgetManager
from reports import ReportGenerator

#Validation inputs
def type_validation(type_s):
    """This method checks if the type is 'income' or 'expense'."""
    if type_s not in ['income', 'expense']:
        print("Error: Please re-enter type (income / expense).")
        return False
    return True


def amount_validation(amount_str):
    """Checks if the input can be converted to a positive float/int."""
    try:
        #Converting string to float and store it
        amount = float(amount_str)

        # Check if the amount is strictly positive
        if amount > 0:
            return True
        else:
            print("Error: Amount must be a positive number greater than 0.")
            return False

    except ValueError:
        print("Error: Amount must be a valid number.")
        return False

def date_validation(date):
    """This method checks if the date input is in correct YYYY-MM-DD format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format.")
        return False

def notblank_validation(text):
    """This method checks if a text input is not blank."""
    if not bool(text and text.strip()):
        print("Error: This field cannot be blank.")
        return False
    return True

#Menu
def menu():
    """
    This method displays the main menu for the Personal Budget Manager,
    gets the user's input, and returns their selection.
    """
    print("===== Personal Budget Manager =====\n")
    print("1. Show all transaction")
    print("2. Add new transaction")
    print("3. Delete transaction")
    print("4. Show total income")
    print("5. Show total expenses")
    print("6. Show current balance")
    print("7. Show expenses by category")
    print("8. Show monthly summary")
    print("9. Save and exit\n")
    choice = input("Choose an option:\n")

    return choice

#Main
def main():
    #Initializing managers
    bm = BudgetManager()
    rg = ReportGenerator()

    #Start the main program loop
    while True:
        choice = menu()

        if choice == '1':
            print("\n--- All Transactions ---")
            transactions = bm.show_all_transactions()
            if transactions is not None:
                print(transactions)

        elif choice == '2':
            t_id = bm.get_next_id()   #Auto-generate the ID, no user input required.
            #Validate Date
            while True:
                date = input("Enter date (YYYY-MM-DD): ")
                if date_validation(date):
                    break

            #Validate Type
            while True:
                # .lower() ensures "Income" or "INCOME" still passes validation
                t_type = input("Enter type (income/expense): ").lower()
                if type_validation(t_type):
                    break

            #Validate Category
            while True:
                category = input("Enter category: ")
                if notblank_validation(category):
                    break

            #Validate Description
            while True:
                desc = input("Enter description: ")
                if notblank_validation(desc):
                    break

            #Validate Amount
            while True:
                amount_input = input("Enter amount: ")
                if amount_validation(amount_input):
                    amount = float(amount_input)
                    break

            #All validations passed! Create and save the transaction.
            new_t = Transaction(t_id, date, t_type, category, desc, amount)
            bm.add_transaction(new_t)

        elif choice == '3':
            print("\n--- Delete Transaction ---")

            #Check if there is data before asking for input
            df = bm.load_from_csv()
            if df.empty:
                print("Error: No transactions available to delete. The file might be missing or empty.")
                continue

            #If it's not empty, safely ask for the ID
            try:
                t_id = int(input("Enter the ID of the transaction to delete: "))
                bm.delete_transaction(t_id)
            except ValueError:
                print("Error: Please enter a valid numerical ID.")

        elif choice == '4':
            income = rg.total_income()

            #Check the variable (using 'is not' is the Python standard for None)
            if income is not None:
                print(f"\nTotal Income: {income:.2f}\n")

        elif choice == '5':
            expense = rg.total_expenses()

            # Check the variable (using 'is not' is the Python standard for None)
            if expense is not None:
                print(f"\nTotal Expenses: {rg.total_expenses():.2f}\n")


        elif choice == '6':
            balance = rg.current_balance()

            # Check the variable (using 'is not' is the Python standard for None)
            if balance is not None:
                print(f"\nCurrent Balance: {rg.current_balance():.2f}\n")


        elif choice == '7':
            df = bm.load_from_csv()
            # Check if the dataframe is empty
            if df.empty:
                print("Expenses by category aren't available.\n")

            else:
                cat = input("\nEnter the category name to search: ")
                total = rg.expenses_by_category(cat)
                if total!=0:
                    print(f"Total spent on '{cat}': {total:.2f}\n")
                else:
                    print(f"No expenses from the {cat} category\n")

        elif choice == '8':
            rg.monthly_summary()

        elif choice == '9':
            print("\nSaving and exiting... Goodbye!")
            break

        else:
            print("\nInvalid option. Please choose a number between 1 and 9.")


#Run the main() function when starting the script
if __name__ == "__main__":
    main()