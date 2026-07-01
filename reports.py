import pandas as pd
import matplotlib.pyplot as plt
from budget_manager import BudgetManager

class ReportGenerator:
    def __init__(self):
        """
        Initializes the ReportGenerator and creates a single instance
        of the BudgetManager to be shared across all report methods.
        """
        self.manager = BudgetManager()

    def total_income(self):
        """Calculates the total sum of all income transactions."""
        df = self.manager.load_from_csv()

        # Check if the dataframe is empty
        if df.empty:
            print("No income available.")
            return None

        #if available - filter for income
        income_df = df[df['type'] == 'income']
        return income_df['amount'].sum()

    def total_expenses(self):
        """Calculates the total sum of all expense transactions."""
        df = self.manager.load_from_csv()

        # Check if the dataframe is empty
        if df.empty:
            print("No expenses available.")
            return None

        #if available - filter for expenses
        expense_df = df[df['type'] == 'expense']
        return expense_df['amount'].sum()

    def current_balance(self):
        """This method returns the current balance by subtracting expenses from income."""
        df = self.manager.load_from_csv()

        # Check if the dataframe is empty
        if df.empty:
            print("Current balance isn't available.")
            return None

        #if the dataframe is not empty
        income = self.total_income()
        exp = self.total_expenses()
        return income-exp

    def expenses_by_category(self,category):
        """Calculates the total sum of all expense transactions by category."""
        df = self.manager.load_from_csv()

        mask = (df['type'] == 'expense') & (df['category'] == category)
        expense_df = df[mask]
        return expense_df['amount'].sum()

    def monthly_summary(self):
        """
        Generates a summary of total income, total expenses, and net savings grouped by month
        + Showing a bar plot
        Expects dates in YYYY-MM-DD format.
        """
        df = self.manager.load_from_csv()

        # Check if the dataframe is empty
        if df.empty:
            print("No transactions available to summarize.")
            return None

        #Converting 'date' to datetime objects, updated format to match YYYY-MM-DD
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')

        #Creating a new column just for the Month and Year (for example: '2025-11')
        df['month_year'] = df['date'].dt.to_period('M')
        print(df)

        #Grouping the data by month and transaction type, then add up the amounts
        summary = df.groupby(['month_year', 'type'])['amount'].sum().unstack(fill_value=0)

        #Safety check: ensure both columns exist in case a month only has one type
        if 'income' not in summary.columns:
            summary['income'] = 0.0
        if 'expense' not in summary.columns:
            summary['expense'] = 0.0

        #Calculating net savings
        summary['net_savings'] = summary['income'] - summary['expense']

        #Calculating averages
        avg_income = summary['income'].mean()
        avg_expense = summary['expense'].mean()
        avg_savings = summary['net_savings'].mean()

        #Print
        print("\n--- Monthly Budget Summary ---")
        print(summary.to_string())
        print("------------------------------")
        print(f"Average Monthly Income:  {avg_income:.2f}")
        print(f"Average Monthly Expense: {avg_expense:.2f}")
        print(f"Average Net Savings:     {avg_savings:.2f}")
        print("------------------------------\n")

        #Generating the Bar Plot
        # Convert the PeriodIndex to strings so Matplotlib formats the x-axis nicely
        plot_data = summary.copy()
        plot_data.index = plot_data.index.astype(str)

        #Creating a grouped bar chart for Income vs Expense
        ax=plot_data[['income', 'expense']].plot(
            kind='bar',
            figsize=(9, 5),
            color=['green', 'red']  # Green for income, Red for expense
        )
        # Loop through each group of bars (containers) and add labels to the top
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3)

        # Labels & Layout
        plt.title('Monthly Income vs Expenses')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.xticks(rotation=45)  #Overlap prevention
        plt.legend(['Income', 'Expense'])
        plt.tight_layout()
        plt.margins(y=0.15)
        plt.show()

        return summary
