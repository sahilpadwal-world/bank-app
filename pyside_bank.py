import sys
import uuid
import datetime
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QComboBox,
    QScrollArea,
    QGridLayout,
)
from PySide6.QtGui import QFont


class BankAccount:
    """
    Represents a single bank account.
    """

    def __init__(
        self, account_holder_name, initial_balance=0.0, account_type="Savings"
    ):
        """
        Initializes a new BankAccount.
        """
        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Initial balance must be a number.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.account_number = str(uuid.uuid4())
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
        self.account_type = account_type
        self.transactions = []
        self.creation_date = datetime.date.today()

    def deposit(self, amount):
        """Deposits money into the account."""
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.balance += amount
        self._add_transaction("Deposit", amount)
        return f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

    def withdraw(self, amount):
        """Withdraws money from the account."""
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)
        return f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"

    def get_balance(self):
        """Returns the current balance of the account."""
        return self.balance

    def get_account_details(self):
        """Returns a string containing the account details."""
        details = f"Account Number: {self.account_number}\n"
        details += f"Account Holder: {self.account_holder_name}\n"
        details += f"Account Type: {self.account_type}\n"
        details += f"Balance: ${self.balance:.2f}\n"
        details += f"Creation Date: {self.creation_date}\n"
        return details

    def _add_transaction(self, transaction_type, amount):
        """Adds a transaction to the transaction history."""
        timestamp = datetime.datetime.now()
        self.transactions.append(
            {"timestamp": timestamp, "type": transaction_type, "amount": amount}
        )

    def get_transaction_history(self):
        """Returns a list of all transactions."""
        return self.transactions

    def format_transaction_history(self):
        """Formats transaction history for display."""
        if not self.transactions:
            return "No transactions yet."

        history_text = "-" * 30 + "\nTransaction History:\n" + "-" * 30 + "\n"
        for transaction in self.transactions:
            history_text += (
                f"{transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - "
                f"{transaction['type']:<10}: ${transaction['amount']:>8.2f}\n"
            )
        history_text += "-" * 30
        return history_text


class BankingSystem:
    """
    Manages multiple bank accounts.
    """

    def __init__(self):
        self.accounts = {}

    def create_account(
        self, account_holder_name, initial_balance=0.0, account_type="Savings"
    ):
        """Creates a new bank account and adds it to the system."""
        try:
            account = BankAccount(account_holder_name, initial_balance, account_type)
            self.accounts[account.account_number] = account
            return f"Account created successfully. Account number: {account.account_number}"
        except (TypeError, ValueError) as e:
            return f"Account creation failed: {e}"

    def get_account(self, account_number):
        """Retrieves a bank account by its account number."""
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        """Deletes a bank account from the system."""
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f"Account {account_number} deleted successfully."
        else:
            return f"Account {account_number} not found."

    def list_all_accounts(self):
        """Returns details for all accounts in the system as formatted text."""
        if not self.accounts:
            return "No accounts in the system."

        accounts_text = "-" * 30 + "\nList of All Accounts:\n" + "-" * 30 + "\n"
        for account_number, account in self.accounts.items():
            accounts_text += account.get_account_details() + "-" * 30 + "\n"
        return accounts_text


class BankingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banking System")
        self.setGeometry(100, 100, 800, 600)  # Adjusted window size
        self.banking_system = BankingSystem()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label = QLabel("Welcome to the Banking System")
        self.title_label.setFont(title_font)
        self.layout.addWidget(self.title_label)

        self.account_number_input = QLineEdit()
        self.account_number_input.setPlaceholderText("Enter Account Number")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Account Holder Name")
        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("Initial Balance (optional)")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.account_type_combo = QComboBox()
        self.account_type_combo.addItems(["Savings", "Checking"])

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        # Create buttons with more descriptive text and tooltips
        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.setToolTip("Create a new bank account")
        self.deposit_button = QPushButton("Deposit")
        self.deposit_button.setToolTip("Deposit money into an account")
        self.withdraw_button = QPushButton("Withdraw")
        self.withdraw_button.setToolTip("Withdraw money from an account")
        self.check_balance_button = QPushButton("Check Balance")
        self.check_balance_button.setToolTip("Check the balance of an account")
        self.account_details_button = QPushButton("Account Details")
        self.account_details_button.setToolTip("View details of an account")
        self.transaction_history_button = QPushButton("Transaction History")
        self.transaction_history_button.setToolTip("View transaction history of an account")
        self.list_accounts_button = QPushButton("List All Accounts")
        self.list_accounts_button.setToolTip("List all accounts in the system")
        self.delete_account_button = QPushButton("Delete Account")
        self.delete_account_button.setToolTip("Delete an existing account")
        self.exit_button = QPushButton("Exit")
        self.exit_button.setToolTip("Exit the application")

        # Connect buttons to actions
        self.create_account_button.clicked.connect(self.create_account)
        self.deposit_button.clicked.connect(self.deposit)
        self.withdraw_button.clicked.connect(self.withdraw)
        self.check_balance_button.clicked.connect(self.check_balance)
        self.account_details_button.clicked.connect(self.get_account_details)
        self.transaction_history_button.clicked.connect(self.get_transaction_history)
        self.list_accounts_button.clicked.connect(self.list_all_accounts)
        self.delete_account_button.clicked.connect(self.delete_account)
        self.exit_button.clicked.connect(self.close)

        # Input Layout (using QGridLayout for better organization)
        input_layout = QGridLayout()
        input_layout.addWidget(QLabel("Account Number:"), 0, 0)
        input_layout.addWidget(self.account_number_input, 0, 1)
        input_layout.addWidget(QLabel("Account Holder Name:"), 1, 0)
        input_layout.addWidget(self.name_input, 1, 1)
        input_layout.addWidget(QLabel("Initial Balance:"), 2, 0)
        input_layout.addWidget(self.balance_input, 2, 1)
        input_layout.addWidget(QLabel("Account Type:"), 3, 0)
        input_layout.addWidget(self.account_type_combo, 3, 1)
        input_layout.addWidget(QLabel("Amount:"), 4, 0)
        input_layout.addWidget(self.amount_input, 4, 1)

        # Button Layout (using QHBoxLayout for horizontal arrangement)
        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.create_account_button)
        button_layout1.addWidget(self.deposit_button)
        button_layout1.addWidget(self.withdraw_button)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.check_balance_button)
        button_layout2.addWidget(self.account_details_button)
        button_layout2.addWidget(self.transaction_history_button)

        button_layout3 = QHBoxLayout()
        button_layout3.addWidget(self.list_accounts_button)
        button_layout3.addWidget(self.delete_account_button)
        button_layout3.addWidget(self.exit_button)


        # Add layouts to main layout
        self.layout.addLayout(input_layout)
        self.layout.addLayout(button_layout1)
        self.layout.addLayout(button_layout2)
        self.layout.addLayout(button_layout3)
        self.layout.addWidget(QLabel("Output:"))
        self.scroll_area = QScrollArea()  # Wrap output in a scroll area
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.output_display)
        self.layout.addWidget(self.scroll_area)


    def display_message(self, message):
        self.output_display.append(message + "\n")

    def clear_output(self):
        self.output_display.clear()

    def get_account_number_input(self):
        account_number = self.account_number_input.text()
        if not account_number:
            QMessageBox.warning(self, "Input Error", "Please enter an account number.")
            return None
        return account_number

    def get_amount_input(self):
        amount_text = self.amount_input.text()
        if not amount_text:
            QMessageBox.warning(self, "Input Error", "Please enter an amount.")
            return None
        try:
            amount = float(amount_text)
            return amount
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid amount. Please enter a number.")
            return None

    def create_account(self):
        name = self.name_input.text()
        initial_balance_text = self.balance_input.text()
        account_type = self.account_type_combo.currentText()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter account holder name.")
            return

        initial_balance = 0.0
        if initial_balance_text:
            try:
                initial_balance = float(initial_balance_text)
            except ValueError:
                QMessageBox.warning(
                    self, "Input Error", "Invalid initial balance. Please enter a number."
                )
                return

        message = self.banking_system.create_account(name, initial_balance, account_type)
        self.display_message(message)
        if "successfully" in message: # Clear inputs only on successful account creation
            self.name_input.clear()
            self.balance_input.clear()
            self.account_number_input.clear() # Clear account number input as it's usually generated


    def deposit(self):
        account_number = self.get_account_number_input()
        amount = self.get_amount_input()
        if not account_number or amount is None:
            return

        account = self.banking_system.get_account(account_number)
        if account:
            try:
                message = account.deposit(amount)
                self.display_message(message)
                self.amount_input.clear() # Clear amount input after successful deposit
            except (TypeError, ValueError) as e:
                QMessageBox.warning(self, "Transaction Error", str(e))
        else:
            QMessageBox.warning(self, "Account Error", "Account not found.")

    def withdraw(self):
        account_number = self.get_account_number_input()
        amount = self.get_amount_input()
        if not account_number or amount is None:
            return

        account = self.banking_system.get_account(account_number)
        if account:
            try:
                message = account.withdraw(amount)
                self.display_message(message)
                self.amount_input.clear() # Clear amount input after successful withdraw
            except (TypeError, ValueError) as e:
                QMessageBox.warning(self, "Transaction Error", str(e))
        else:
            QMessageBox.warning(self, "Account Error", "Account not found.")

    def check_balance(self):
        account_number = self.get_account_number_input()
        if not account_number:
            return

        account = self.banking_system.get_account(account_number)
        if account:
            balance = account.get_balance()
            self.display_message(f"Current balance: ${balance:.2f}")
        else:
            QMessageBox.warning(self, "Account Error", "Account not found.")

    def get_account_details(self):
        account_number = self.get_account_number_input()
        if not account_number:
            return

        account = self.banking_system.get_account(account_number)
        if account:
            details = account.get_account_details()
            self.display_message(details)
        else:
            QMessageBox.warning(self, "Account Error", "Account not found.")

    def get_transaction_history(self):
        account_number = self.get_account_number_input()
        if not account_number:
            return

        account = self.banking_system.get_account(account_number)
        if account:
            history_text = account.format_transaction_history()
            self.display_message(history_text)
        else:
            QMessageBox.warning(self, "Account Error", "Account not found.")

    def list_all_accounts(self):
        accounts_text = self.banking_system.list_all_accounts()
        self.display_message(accounts_text)

    def delete_account(self):
        account_number = self.get_account_number_input()
        if not account_number:
            return

        message = self.banking_system.delete_account(account_number)
        self.display_message(message)
        self.account_number_input.clear() # Clear account number input after delete attempt


if __name__ == "__main__":
    app = QApplication(sys.argv)
    banking_app = BankingApp()
    banking_app.show()
    sys.exit(app.exec())