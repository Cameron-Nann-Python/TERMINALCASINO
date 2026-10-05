from textual.app import App, ComposeResult
from textual import on
from textual.widgets import Header, Footer, Input, Label
from textual.screen import Screen, ModalScreen
from textual.containers import VerticalScroll
from textual.binding import Binding

class Content(VerticalScroll):
    """Vertical Scrollbar"""

class GetUserName(ModalScreen):
    """Allows user to input name"""
    def compose(self):
        yield Input(placeholder="Enter your name: ")

    @on(Input.Submitted)
    def accept_user_name(self, event: Input.Submitted):
        # removes pop up
        self.dismiss(event.value)

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Content(id="homecontent"):
            yield Header(id="mainheader")
            yield Label("", id="username")
            yield Footer()

    def set_username(self, username):
        self.query_one("#username", Label).update(username)

    def on_mount(self):
        self.title = "♦ T E R M I N A L  C A S I N O ♦"
        self.app.push_screen(GetUserName(), self.set_username)

class TerminalCasinoApp(App):
    CSS_PATH = "casinotxt.tcss"
    SCREENS = {
        "home" : HomeScreen
    }
    BINDINGS = [
        Binding("E", "enter", "[E]nter"),
        Binding("Q", "quit", "[Q]uit")
    ]

    def compose(self) -> ComposeResult:
        yield Footer()

    def on_mount(self):
        self.push_screen("home")

    # capture key events
    def action_quit(self):
        self.exit()

if __name__ == "__main__":
    app = TerminalCasinoApp()
    app.run()