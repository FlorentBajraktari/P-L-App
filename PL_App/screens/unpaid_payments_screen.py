from kivymd.uix.behaviors.toggle_behavior import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from utils.data_management import unpaid_payments


class UnpaidPaymentsScreen(MDScreen):
    def on_enter(self):
        self.populate_unpaid_payments_list()

    def populate_unpaid_payments_list(self):
        self.ids.unpaid_payments_list.clear_widgets()
        for payment in unpaid_payments:
            self.ids.unpaid_payments_list.add_widget(OneLineListItem(
                text=f"{payment['name']} - ${payment['amount']}"))

    def add_unpaid_payment(self):
        new_payment = {
            "name": f"Unpaid Item {len(unpaid_payments) + 1}", "amount": 50}
        unpaid_payments.append(new_payment)
        self.populate_unpaid_payments_list()

    def update_unpaid_payment(self):
        if unpaid_payments:
            unpaid_payments[-1]["name"] = f"Updated Unpaid Item {len(unpaid_payments)}"
            unpaid_payments[-1]["amount"] += 25
            self.populate_unpaid_payments_list()
        else:
            self.show_dialog("Update Payment", "No unpaid payments to update.")

    def delete_unpaid_payment(self):
        if unpaid_payments:
            unpaid_payments.pop()
            self.populate_unpaid_payments_list()
        else:
            self.show_dialog("Delete Payment", "No unpaid payments to delete.")

    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(
                text="Close", on_release=lambda _: self.dialog.dismiss())]
        )
        self.dialog.open()
