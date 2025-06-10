from textual import containers
from textual.app import ComposeResult
from textual.widgets import (
    Tree,
)


class ScanGrid(containers.VerticalGroup):
    DEFAULT_CLASSES = "column"

    DEFAULT_CSS = """
    ScanGrid {
        padding-top: 1;
        layout: grid;
        grid-size: 1;
        height: 70%;       
        Tree {
            padding: 1;
            &.-maximized { height: 1fr; }    
            border: wide transparent;            
            border-title-align: center;
            &:focus { border: wide $border; }        
        }
    }

    """

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
