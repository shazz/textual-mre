import json

from textual.app import App, ComposeResult
from textual.widgets import Header

from screens.load_screen import LoadScreen, PathEntered
from screens.main_screen import MainScreen
from textual.demo.data import MOVIES_JSON


class TuiApp(App):
    BINDINGS = [
        ("l", "select_directory", "Select directory"),
    ]
    SCREENS = {
        "main": MainScreen,
        "load": LoadScreen,
    }

    def compose(self) -> ComposeResult:
        yield Header()

    def get_default_screen(self):
        return MainScreen()

    def action_select_directory(self) -> None:
        """Action to select a directory."""

        self.push_screen(LoadScreen())

    def on_path_entered(self, event: PathEntered) -> None:
        # This handler fires when PathModal posts PathEntered

        if event.path:
            #  call an external API here to get the tree content based on PathEntered
            tree_data = json.loads(MOVIES_JSON)

            # main_screen: MainScreen = self.get_screen("main")
            main_screen: MainScreen = self.query_one(MainScreen)
            main_screen.update_tree(tree_data=tree_data)
