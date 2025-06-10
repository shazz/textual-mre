import os

from textual.app import ComposeResult
from textual.containers import Grid
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Input


class PathEntered(Message):
    """A custom Message carrying the user-entered path."""

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()


class ModalPathInput(Input):
    """Input widget to select directory."""

    def on_mount(self):
        self.placeholder = "Enter path  here..."
        self.value = os.getcwd()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        self.notify(f"Selected folder: {event.value}")

        # send message if input ss submitted (Enter pressed, not button)
        self.app.post_message(PathEntered(event.value))

        # close modal screen
        self.app.pop_screen()


class LoadScreen(ModalScreen[bool]):
    CSS_PATH = "load_screen.tcss"

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
