from datetime import date
from enum import Enum
from os.path import dirname
from sqlite3 import Connection, connect, IntegrityError

import sport_tracker
from sport_tracker.common.exceptions import IllegalArgumentException


class ActivityLevel(Enum):
    SEDENTARY = 1
    MODERATE = 2
    VIGOROUS = 3
    EXTREME = 4


class DBController:
    def __init__(self):
        self.db_file: str = f"{dirname(sport_tracker.__file__)}/model/database.db"
        self.connection: Connection = self.create_connection()
        self.statements = {"UPDATE": "TODO",
                           "INSERT_USER": "INSERT INTO users('name', 'born_date', 'weight', 'height', activity_level) "
                                          "VALUES (?, ?, ?, ?, ?)",
                           "INSERT_ACTIVITY": "INSERT INTO activities('sport_id', 'user_id', 'time', 'distance') "
                                              "VALUES (?, ?, ?, ?)",
                           "INSERT_SPORT": "INSERT INTO sports('name', 'moving') VALUES (?, ?)",
                           "DELETE": "",
                           "FETCH": "SELECT ? FROM ? WHERE ?=?",
                           "FETCH_ALL": "SELECT * FROM ?"}

    def create_connection(self) -> Connection:
        return connect(self.db_file)

    def _execute(self, statement: str, *args):
        if statement not in self.statements:
            raise IllegalArgumentException(f"statement argument must be one of the {self.statements.keys()}")
        c = self.connection.cursor()
        try:
            c.execute(self.statements[statement], args)
        except IntegrityError as e:
            raise
        else:
            self.connection.commit()
        finally:
            self.connection.close()

    def insert_user(self, *, name: str, date_born: date, weight: float, height: int, activity: ActivityLevel):
        self._execute("INSERT_USER", name, date_born.strftime("%Y-%m-%d"), weight, height, activity.value)


if __name__ == '__main__':
    db = DBController()
    db.insert_user(name="Arthur Dent", date_born=date.today(), weight=75.6, height=178, activity=ActivityLevel.MODERATE)
