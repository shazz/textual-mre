import json
import os
from typing import Dict
from textual import containers, lazy
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.demo.data import MOVIES_JSON
from textual.demo.page import PageScreen
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Input, Tree


class ScanGrid(containers.VerticalGroup):
    def compose(self) -> ComposeResult:
        tree = Tree("List results", classes="box")
        tree.show_root = False
        tree.add_json({})
        tree.root.expand()

        yield tree

    def update_tree(self, data: dict) -> None:
        tree = self.query_one(Tree)
        tree.clear()
        tree.add_json(data)
        tree.root.expand()


class PathEntered(Message):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()


class ModalPathInput(Input):
    def on_mount(self):
        self.placeholder = "Enter path  here..."
        self.value = os.getcwd()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.notify(f"Selected folder: {event.value}")

        # send message if input ss submitted (Enter pressed, not button)
        self.app.post_message(PathEntered(event.value))
        self.app.pop_screen()


class LoadScreen(ModalScreen[bool]):
    CSS = """
        LoadScreen {
        align: center middle;
    }

    #dialog {
        layout: grid;
        grid-size: 2 2;
        grid-rows: 3 3;
        padding: 1 1 0 1;
        width: 60;
        height: 9;
        border: solid white 70%;
        background: $surface;
    }

    #input {
        column-span: 2;
        border: solid white 70%;
        padding: 0;
        margin: 0;
    }

    #ok, #cancel {
        width: 100%;
        padding: 0;
        margin: 0 1 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            ModalPathInput(placeholder="Enter path here...", id="input", type="text"),
            Button("Ok", variant="success", id="ok"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            input_widget = self.query_one(ModalPathInput)
            path = input_widget.value.strip()

            # send mesage if button is explicitely clicked
            self.app.post_message(PathEntered(path))

        self.app.pop_screen()


class MainScreen(PageScreen):
    def compose(self) -> ComposeResult:
        with lazy.Reveal(containers.VerticalScroll(can_focus=True)):
            yield ScanGrid()
        yield Footer()

    def on_mount(self) -> None:
        self.tree_data: Dict = {}

    def update_tree(self, tree_data: Dict) -> None:
        scan_grid = self.query_one(ScanGrid)
        scan_grid.update_tree(data=tree_data)

        self.tree_data = tree_data


class TuiApp(App):
    BINDINGS = [
        ("l", "select_directory", "Select directory"),
    ]
    SCREENS = {
        "main": MainScreen,
        "load": LoadScreen,
    }

    def get_default_screen(self):
        return MainScreen()

    def action_select_directory(self) -> None:
        self.push_screen(LoadScreen())

    def on_path_entered(self, event: PathEntered) -> None:
        if event.path:
            #  call an external API here to get the tree content based on PathEntered
            tree_data = json.loads(MOVIES_JSON)

            # main_screen: MainScreen = self.get_screen("main")
            main_screen: MainScreen = self.query_one(MainScreen)
            main_screen.update_tree(tree_data=tree_data)


if __name__ == "__main__":
    app = TuiApp()
    app.run()
