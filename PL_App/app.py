import csv
import os
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout

# Paths for CSV files
PAID_PAYMENTS_FILE = "paid_payments.csv"
UNPAID_PAYMENTS_FILE = "unpaid_payments.csv"
BUDGET_FILE = "budget.csv"

# Sample user data for login
users = [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    {"username": "user3", "password": "pass3"}
]

# Load and save functions for CSV


def load_csv_data(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    return data


def save_csv_data(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Load payment data from CSV files
paid_payments = load_csv_data(PAID_PAYMENTS_FILE)
unpaid_payments = load_csv_data(UNPAID_PAYMENTS_FILE)

# Load budget data or set a default budget if none exists
budget_data = load_csv_data(BUDGET_FILE)
if not budget_data:
    budget_data = [{"monthly_budget": "1000.00"}]
    save_csv_data(BUDGET_FILE, budget_data, fieldnames=["monthly_budget"])

# Login screen


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(
            MDLabel(text="Login", halign="center", font_style="H4"))

        self.username_input = MDTextField(hint_text="Username")
        self.password_input = MDTextField(hint_text="Password", password=True)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        layout.add_widget(MDRaisedButton(
            text="Login", on_release=self.verify_login))
        self.add_widget(layout)

    def verify_login(self, *args):
        username, password = self.username_input.text, self.password_input.text
        for user in users:
            if user["username"] == username and user["password"] == password:
                self.manager.current = "main_menu"
                return
        self.show_error_dialog()

    def show_error_dialog(self):
        self.dialog = MDDialog(
            title="Login Failed",
            text="Invalid credentials.",
            buttons=[MDFlatButton(
                text="Close", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

# Main menu screen


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(
            MDLabel(text="WELCOME", halign="center", font_style="H4"))

        buttons = [
            ("View P&L Statement", self.open_pnl_statement),
            ("Set Monthly Budget", self.open_budget),
            ("Manage Paid Payments", self.open_paid_payments),
            ("Manage Unpaid Payments", self.open_unpaid_payments),
            ("Sign Out", self.sign_out)
        ]

        for text, callback in buttons:
            layout.add_widget(MDRaisedButton(text=text, on_release=callback))
        self.add_widget(layout)

    def open_pnl_statement(self, *args):
        self.manager.current = "pnl_statement"

    def open_budget(self, *args):
        self.manager.current = "budget"

    def open_paid_payments(self, *args):
        self.manager.current = "paid_payments"

    def open_unpaid_payments(self, *args):
        self.manager.current = "unpaid_payments"

    def sign_out(self, *args):
        self.manager.current = "login_screen"

# P&L Statement screen


class PnLStatementScreen(Screen):
    def on_enter(self):
        self.show_pnl_statement()

    def show_pnl_statement(self):
        total_income = sum(float(payment["amount"])
                           for payment in paid_payments)
        total_expense = sum(float(payment["amount"])
                            for payment in unpaid_payments)
        monthly_budget = float(budget_data[0]["monthly_budget"])
        net_balance = monthly_budget - total_income - total_expense

        dialog_text = (f"Monthly Budget: ${monthly_budget:.2f}\n"
                       f"Total Income (Paid): ${total_income:.2f}\n"
                       f"Total Expenses (Unpaid): ${total_expense:.2f}\n"
                       f"Remaining Balance: ${net_balance:.2f}")
        self.dialog = MDDialog(
            title="P&L Statement",
            text=dialog_text,
            buttons=[MDFlatButton(text="Back", on_release=self.back_to_menu)]
        )
        self.dialog.open()

    def back_to_menu(self, *args):
        self.dialog.dismiss()
        self.manager.current = "main_menu"

# Budget screen for setting monthly budget


class BudgetScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(MDLabel(text="Set Monthly Budget",
                          halign="center", font_style="H5"))

        # Budget input field
        self.budget_input = MDTextField(
            hint_text="Enter Monthly Budget", multiline=False)
        if budget_data:
            self.budget_input.text = budget_data[0]["monthly_budget"]
        layout.add_widget(self.budget_input)

        layout.add_widget(MDRaisedButton(
            text="Save Budget", on_release=self.save_budget))
        layout.add_widget(MDRaisedButton(
            text="Back to Menu", on_release=self.back_to_menu))
        self.add_widget(layout)

    def save_budget(self, *args):
        budget_data[0]["monthly_budget"] = self.budget_input.text
        save_csv_data(BUDGET_FILE, budget_data, fieldnames=["monthly_budget"])

        # Confirmation dialog
        self.dialog = MDDialog(
            title="Success",
            text="Monthly budget saved.",
            buttons=[MDFlatButton(
                text="Close", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def back_to_menu(self, *args):
        self.manager.current = "main_menu"

# Payment management screen for handling both paid and unpaid payments


class PaymentManagementScreen(Screen):
    def __init__(self, payment_type, **kwargs):
        super().__init__(**kwargs)
        self.payment_type = payment_type
        self.selected_item = None

        layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        layout.add_widget(
            MDLabel(text=f"{payment_type} Payments", halign="center", font_style="H5"))

        # Input fields
        self.amount_input = MDTextField(hint_text="Amount", multiline=False)
        self.description_input = MDTextField(
            hint_text="Description", multiline=False)
        layout.add_widget(self.amount_input)
        layout.add_widget(self.description_input)

        # List and scrolling area
        self.payment_list = MDList()
        scroll = ScrollView()
        scroll.add_widget(self.payment_list)
        layout.add_widget(scroll)

        # Action buttons
        action_layout = MDBoxLayout(
            size_hint_y=None, height="50dp", spacing=10)
        action_layout.add_widget(MDRaisedButton(
            text="Add", on_release=self.add_payment))
        action_layout.add_widget(MDRaisedButton(
            text="Update", on_release=self.update_payment))
        action_layout.add_widget(MDRaisedButton(
            text="Delete", on_release=self.delete_payment))

        if self.payment_type == "Unpaid":
            action_layout.add_widget(MDRaisedButton(
                text="Transfer to Paid", on_release=self.transfer_to_paid))

        layout.add_widget(action_layout)
        layout.add_widget(MDRaisedButton(
            text="Back to Menu", on_release=self.back_to_menu))
        self.add_widget(layout)

    def on_enter(self):
        self.populate_list()

    def populate_list(self):
        self.payment_list.clear_widgets()
        payment_data = unpaid_payments if self.payment_type == "Unpaid" else paid_payments
        for payment in payment_data:
            item = OneLineListItem(
                text=f"{payment['description']} - ${payment['amount']}", on_release=self.select_item)
            self.payment_list.add_widget(item)

    def add_payment(self, *args):
        item = {"description": self.description_input.text,
                "amount": self.amount_input.text}
        target_data = unpaid_payments if self.payment_type == "Unpaid" else paid_payments
        target_data.append(item)

        file_path = UNPAID_PAYMENTS_FILE if self.payment_type == "Unpaid" else PAID_PAYMENTS_FILE
        save_csv_data(file_path, target_data, fieldnames=[
                      "description", "amount"])
        self.populate_list()
        self.clear_inputs()

    def update_payment(self, *args):
        if self.selected_item:
            selected_text = self.selected_item.text
            payment_data = unpaid_payments if self.payment_type == "Unpaid" else paid_payments
            for i, payment in enumerate(payment_data):
                if selected_text == f"{payment['description']} - ${payment['amount']}":
                    payment_data[i] = {
                        "description": self.description_input.text, "amount": self.amount_input.text}
                    break
            file_path = UNPAID_PAYMENTS_FILE if self.payment_type == "Unpaid" else PAID_PAYMENTS_FILE
            save_csv_data(file_path, payment_data, fieldnames=[
                          "description", "amount"])
            self.populate_list()
            self.clear_inputs()

    def delete_payment(self, *args):
        if self.selected_item:
            selected_text = self.selected_item.text
            payment_data = unpaid_payments if self.payment_type == "Unpaid" else paid_payments
            payment_data[:] = [
                payment for payment in payment_data if f"{payment['description']} - ${payment['amount']}" != selected_text]
            file_path = UNPAID_PAYMENTS_FILE if self.payment_type == "Unpaid" else PAID_PAYMENTS_FILE
            save_csv_data(file_path, payment_data, fieldnames=[
                          "description", "amount"])
            self.populate_list()
            self.clear_inputs()

    def transfer_to_paid(self, *args):
        if self.selected_item:
            selected_text = self.selected_item.text
            for i, payment in enumerate(unpaid_payments):
                if selected_text == f"{payment['description']} - ${payment['amount']}":
                    paid_payments.append(payment)
                    del unpaid_payments[i]
                    break
            save_csv_data(UNPAID_PAYMENTS_FILE, unpaid_payments,
                          fieldnames=["description", "amount"])
            save_csv_data(PAID_PAYMENTS_FILE, paid_payments,
                          fieldnames=["description", "amount"])
            self.populate_list()

    def select_item(self, item):
        self.selected_item = item
        description, amount = item.text.split(" - $")
        self.description_input.text = description
        self.amount_input.text = amount

    def clear_inputs(self):
        self.selected_item = None
        self.description_input.text = ""
        self.amount_input.text = ""

    def back_to_menu(self, *args):
        self.manager.current = "main_menu"

# Main app class


class PnLApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(PnLStatementScreen(name="pnl_statement"))
        sm.add_widget(BudgetScreen(name="budget"))
        sm.add_widget(PaymentManagementScreen(
            name="paid_payments", payment_type="Paid"))
        sm.add_widget(PaymentManagementScreen(
            name="unpaid_payments", payment_type="Unpaid"))
        return sm


if __name__ == "__main__":
    PnLApp().run()
