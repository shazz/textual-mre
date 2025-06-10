from typing import Dict

from textual import containers, lazy
from textual.app import ComposeResult
from textual.binding import Binding
from textual.demo.page import PageScreen
from textual.widgets import Footer

from widgets.scan_grid import ScanGrid


class MainScreen(PageScreen):
    """The Main screen"""

    CSS = """
    MainScreen { 
        align-horizontal: center;
        & > VerticalScroll {
            scrollbar-gutter: stable;
            & > * {                          
                &:even { background: $boost; }
                padding-bottom: 1;
            }
        }
    }
    """

    BINDINGS = [Binding("escape", "blur", "Unfocus any focused widget", show=False)]

    def compose(self) -> ComposeResult:
        with lazy.Reveal(containers.VerticalScroll(can_focus=True)):
            yield ScanGrid()
        yield Footer()

    def on_mount(self) -> None:
        self.tree_data: Dict = {}

    def update_tree(self, tree_data: Dict) -> None:
        """Update the scan tree with new data."""

        scan_grid = self.query_one(ScanGrid)
        scan_grid.update_tree(data=tree_data)

        self.tree_data = tree_data
