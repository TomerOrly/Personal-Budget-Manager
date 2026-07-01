import pandas as pd
from models import Transaction

class BudgetManager:
    def __init__(self):
        #storing filename and columns as class attributes
        self.filepath = 'transactions.csv'
        self.columns = ['id', 'date', 'type', 'category', 'description', 'amount']

    def load_from_csv(self):
        """
        This method loads transactions from csv file (with the filepath).
        If not exist - it will generate new one
        """
        try:
            df = pd.read_csv(self.filepath)
            return df

        except FileNotFoundError:
            print(f'No {self.filepath} found, generating new one.')

            #Creating an empty DataFrame with the specific columns first, then saving it as a new CSV file.
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filepath, index=False)
            return df

    def save_to_csv(self,df):
        """
        This method saves the dataframe to csv file.
        """
        df.to_csv(self.filepath, index=False)

    def get_next_id(self):
        """
        Calculates the next available transaction ID.
        If the CSV is empty, it starts at 1. Otherwise, it finds the max ID and adds 1.
        """
        df = self.load_from_csv()

        if df.empty:
            return 1
        else:
            # Grab the maximum value in the 'id' column and add 1
            return int(df['id'].max()) + 1

    def add_transaction(self, transaction):
        """
        Adds a new transaction to the CSV file.

        This method gets a Transaction object, extracts
        its data, and checks if the transaction ID is unique. If the ID is unique,
        it appends the new transaction to the existing records and saves the
        updated data back to the CSV.
        """
        df = self.load_from_csv()

        if isinstance(transaction, dict):
            transaction_data = transaction
        else:
            transaction_data = transaction.to_dict()

        new_id = transaction_data['id']

        if new_id in df['id'].values:
            print(f"Error: Transaction with ID {new_id} already exists! Canceling.\n")
            return df

        transaction_df = pd.DataFrame([transaction_data])
        final_df = pd.concat([df, transaction_df], ignore_index=True)

        self.save_to_csv(final_df)
        print(f"Success: Transaction with ID {new_id} added.\n")
        return final_df

    def delete_transaction(self, transaction):
        """
        This method deletes a transaction from the CSV file using its unique ID.
        The method gets a transaction id parameter and checks the current records for the specified transaction ID.
        If found, the record is removed and the updated data is saved to the CSV,
        followed by a success message. If the ID does not exist, an error message
        is displayed to the user.
        """

        df = self.load_from_csv()
        #If the file didn't exist (or is completely empty), stop here.
        if df.empty:
            print("Error: No transactions available to delete. The file might be missing or empty.\n")
            return

        #Safely extract the target ID (handling both dicts and objects)
        if isinstance(transaction, dict):
            target_id = transaction['id']
        else:
            target_id = transaction.id

        #Checking if the ID exists
        if target_id in df['id'].values:
            #Filtering instead of drop: Keep all rows where 'id' is NOT the target_id
            df = df[df['id'] != target_id]

            #Saving the updated dataframe
            self.save_to_csv(df)

            #Messages to the user
            print(f"Success: Transaction {target_id} deleted.\n")
        else:
            print(f"Error: Transaction with id {target_id} not found.\n")

    def show_all_transactions(self):
        try:
            df = pd.read_csv(self.filepath)

            # Check if the dataframe is empty
            if df.empty:
                print("No Transactions.\n")
                return None

            return df

        except FileNotFoundError:
            print(f'No {self.filepath} found.\n')
