from textual.app import App
from textual.widgets import Label, Static

class TerminalCasinoApp(App):
    # store widgets, does not display
    def compose(self):
        # manually turn off bold and red
        self.static = Static("I am a [bold red]Static[/bold red] widget")
        yield self.static
        # / turns off all attributes
        self.label = Label("I am a [yello italic]Label[/] widget")
        yield self.label

    def on_mount(self):
        # Style the Static widget
        self.static.styles.background = "blue"
        self.static.styles.border = ("solid", "white")
        # python uses underscores instead of hyphens
        self.static.styles.text_align = "center"
        self.static.styles.padding = 1, 1
        self.static.styles.margin = 4, 4

        # Style the Label widget
        self.label.styles.background = "darkgreen"
        self.label.styles.border = ("double", "red")
        self.label.styles.padding = 1, 1
        self.label.styles.margin = 2, 4

    # capture key events
    def on_key(self, event):
        match event.key:
            case "q":
                exit()


if __name__ == "__main__":
    app = TerminalCasinoApp()
    app.run()