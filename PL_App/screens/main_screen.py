from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main_screen"
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation="horizontal", padding=10, spacing=10)

        # Left side buttons
        left_layout = MDBoxLayout(
            orientation="vertical", size_hint_x=0.3, spacing=10)

        # Define main buttons with actions
        view_pnl_button = MDRaisedButton(
            text="View P&L Statement",
            on_release=lambda _: self.parent.app.view_pnl_statement()
        )
        settings_button = MDRaisedButton(
            text="Settings",
            on_release=lambda _: self.parent.app.open_settings()
        )
        paid_button = MDRaisedButton(
            text="Paid Payments",
            on_release=lambda _: self.parent.app.open_paid_payments()
        )
        unpaid_button = MDRaisedButton(
            text="Unpaid Payments",
            on_release=lambda _: self.parent.app.open_unpaid_payments()
        )
        logout_button = MDRaisedButton(
            text="Logout",
            on_release=lambda _: self.parent.app.logout()
        )

        # Add buttons to the left layout
        for button in [view_pnl_button, settings_button, paid_button, unpaid_button, logout_button]:
            left_layout.add_widget(button)

        # Right side content area
        right_layout = MDBoxLayout(
            orientation="vertical", spacing=10, padding=10)

        title = MDLabel(text="Data List", halign="center", font_style="H5")
        right_layout.add_widget(title)

        # Add ScrollView for the list of items
        scroll_view = ScrollView()
        self.item_list = MDList()
        scroll_view.add_widget(self.item_list)
        right_layout.add_widget(scroll_view)

        # Action buttons for Add, Update, Delete
        action_buttons_layout = MDBoxLayout(
            size_hint_y=None, height="40dp", spacing=10)

        add_button = MDRectangleFlatButton(
            text="Add", on_release=lambda _: self.parent.app.add_item())
        update_button = MDRectangleFlatButton(
            text="Update", on_release=lambda _: self.parent.app.update_item())
        delete_button = MDRectangleFlatButton(
            text="Delete", on_release=lambda _: self.parent.app.delete_item())

        for button in [add_button, update_button, delete_button]:
            action_buttons_layout.add_widget(button)

        right_layout.add_widget(action_buttons_layout)

        # Add left and right layouts to main layout
        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)
