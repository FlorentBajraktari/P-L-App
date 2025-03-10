from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder

# Users for demo purposes
users = {"user1": "pass1", "user2": "pass2", "user3": "pass3"}

# Updated LoginScreen with KivyMD components


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        layout.add_widget(
            MDLabel(text="Login", halign="center", font_style="H4"))

        self.username_input = MDTextField(
            hint_text="Username",
            icon_right="account",
            mode="rectangle"
        )
        self.password_input = MDTextField(
            hint_text="Password",
            icon_right="lock",
            password=True,
            mode="rectangle"
        )

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        login_button = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5},
            on_release=self.verify_login
        )

        layout.add_widget(login_button)
        self.add_widget(layout)

    def verify_login(self, *args):
        username = self.username_input.text
        password = self.password_input.text
        if username in users and users[username] == password:
            self.manager.current = "main_menu"
        else:
            dialog = MDDialog(
                title="Login Failed",
                text="Incorrect username or password.",
                buttons=[MDRaisedButton(
                    text="Close", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()

# Main menu screen (as a placeholder)


class MainMenuScreen(Screen):
    pass

# Main App Class


class PnLApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login_screen"))
        sm.add_widget(MainMenuScreen(name="main_menu"))

        return sm


if __name__ == "__main__":
    PnLApp().run()
