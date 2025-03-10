from kivymd.uix.behaviors.toggle_behavior import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from utils.data_management import paid_payments


class PaidPaymentsScreen(MDScreen):
    def on_enter(self):
        self.populate_paid_payments_list()

    def populate_paid_payments_list(self):
        self.ids.paid_payments_list.clear_widgets()
        for payment in paid_payments:
            self.ids.paid_payments_list.add_widget(OneLineListItem(
                text=f"{payment['name']} - ${payment['amount']}"))

    def add_paid_payment(self):
        new_payment = {
            "name": f"Paid Item {len(paid_payments) + 1}", "amount": 100}
        paid_payments.append(new_payment)
        self.populate_paid_payments_list()

    def update_paid_payment(self):
        if paid_payments:
            paid_payments[-1]["name"] = f"Updated Paid Item {len(paid_payments)}"
            paid_payments[-1]["amount"] += 50
            self.populate_paid_payments_list()
        else:
            self.show_dialog("Update Payment", "No paid payments to update.")

    def delete_paid_payment(self):
        if paid_payments:
            paid_payments.pop()
            self.populate_paid_payments_list()
        else:
            self.show_dialog("Delete Payment", "No paid payments to delete.")

    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(
                text="Close", on_release=lambda _: self.dialog.dismiss())]
        )
        self.dialog.open()
