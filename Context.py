from __future__ import annotations
from Position import Position


class Context:
    def __init__(self, display_name, parent: Context = None, parent_entry_pos: Position = None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
