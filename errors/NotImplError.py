from Position import Position
from errors.Error import Error


class NotImplError(Error):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        super().__init__(pos_start, pos_end, "Not implemented", details)
