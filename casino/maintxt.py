from textual.app import App, ComposeResult
from textual.widgets import Header, Label, Static, Button, Markdown, Footer
from textual.screen import Screen, ModalScreen
from textual.containers import Container, VerticalScroll
from textual.binding import Binding

class Content(VerticalScroll):
    """Vertical Scrollbar"""

class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        with Content():
            yield Header(id="mainheader")
            yield Footer()

    def on_mount(self):
        self.title = "♦ T E R M I N A L  C A S I N O ♦"

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
    def on_key(self, event):
        match event.key:
            case "q":
                exit()


if __name__ == "__main__":
    app = TerminalCasinoApp()
    app.run()