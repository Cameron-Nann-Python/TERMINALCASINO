from textual.app import App, ComposeResult
from textual import on
from textual.widgets import Header, Footer, Input, Label, Button, Static
from textual.screen import Screen, ModalScreen
from textual.containers import VerticalScroll, Container, Horizontal
from textual.binding import Binding
from typing import cast

import shutil
from typing import Callable
from . import games
from .accounts import Account
from .config import Config
from .types import GameContext
from .utils import cprint, cinput, clear_screen, display_topbar, get_theme

GAME_HANDLERS: dict[str, Callable[[GameContext], None]] = {
    "blackjack (U.S.)": games.blackjack.play_blackjack,
    "blackjack (E.U.)": games.blackjack.play_european_blackjack,
    "slots": games.slots.play_slots,
    "slots (Expanded)": games.slots.play_slots_expanded,
    "poker": games.poker.play_poker,
    "roulette": games.roulette.play_roulette,
    "uno": games.uno.play_uno,
    "european roulette": games.roulette.play_european_roulette,
}
ALL_GAMES = list(GAME_HANDLERS.keys())

ACCOUNT_STARTING_BALANCE = 100

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
        with Content(id="home_content"):
            yield Header(id="main_header")
            with Horizontal(id="name_account"):
                yield Label("", id="username")
                yield Static("", id="spacer")
                yield Label(str(ACCOUNT_STARTING_BALANCE), id="account_balance")
            with Container(id="game_content"):
                yield Label("Please choose a game to play:", id="choose_game_prompt")
                for i, game in enumerate(ALL_GAMES):
                    yield Button(game.capitalize(), id=f"game_{i+1}", classes="games")
                    i += 1

            yield Footer()

    def set_username(self, username):
        self.query_one("#username", Label).update(username)
        app = cast(TerminalCasinoApp, self.app) # cast for realtime css updates
        app.username = username

    def on_mount(self):
        self.title = "♦ T E R M I N A L  C A S I N O ♦"
        self.app.push_screen(GetUserName(), self.set_username)

    @on(Button.Pressed)
    def play_game(self, event: Button.Pressed):
        app = cast(TerminalCasinoApp, self.app)
        app.selected_game = str(event.button.id)[-1]
        self.app.exit()

class TerminalCasinoApp(App):
    selected_game = ""
    username = ""
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
    name = app.username
    account = Account.generate(name, ACCOUNT_STARTING_BALANCE)

    def play_game(result, account):
        config = Config.default()
        ctx = GameContext(account=account, config=config)
        selected_game = ALL_GAMES[int(result) - 1]
        handler = GAME_HANDLERS.get(selected_game)
        if handler:
            clear_screen()
            handler(ctx)  # returns to loop after game finishes

    play_game(app.selected_game, account)
