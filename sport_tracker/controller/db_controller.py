from os.path import dirname
from sqlite3 import Connection, connect

from sport_tracker.common.exceptions import IllegalArgumentException


class DBController:
    def __init__(self):
        self.db_file: str = f"{dirname(self.__file__)}/../model/database.db"
        self.connection: Connection = self.create_connection()
        self.statements = {"UPDATE": "TODO",
                           "INSERT": "",
                           "DELETE": "",
                           "FETCH": "SELECT ? FROM ? WHERE ?=?"}

    def create_connection(self) -> Connection:
        return connect(self.db_file)

    def execute(self, statement: str, *args):
        if statement not in self.statements:
            raise IllegalArgumentException(f"statement argument must be one of the {self.statements.keys()}")
        with self.connection.cursor() as c:
            c.exeute(self.statements[statement], *args)
