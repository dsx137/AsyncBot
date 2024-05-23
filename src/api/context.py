from .event import Bus
from .db import Db


class Context:
    pass


class _ContextProgram(Context):
    def __init__(self, bus: Bus, db: Db) -> None:
        self.bus = bus
        self.db = db
        self.db.create_table(
            "candidate",
            {
                "name": "TEXT",
                "url": "TEXT",
                "description": "TEXT",
            },
        )


program: _ContextProgram = None


def init_program(bus: Bus, db: Db) -> None:
    global program
    program = _ContextProgram(bus=bus, db=db)
