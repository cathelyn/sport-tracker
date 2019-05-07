from datetime import date
from os.path import dirname
from sqlite3 import Connection, connect, IntegrityError

import sport_tracker
from sport_tracker.common.exceptions import IllegalArgumentException
from sport_tracker.model.person import ActivityLevel


class DBController:
    def __init__(self):
        self.db_file: str = f"{dirname(sport_tracker.__file__)}/model/database.db"  # db file is auto-created
        self.connection: Connection = self.create_connection()
        self.statements = {"UPDATE": "TODO",
                           "INSERT_USER": "INSERT INTO users('name', 'born_date', 'weight', 'height', activity_level) "
                                          "VALUES (?, ?, ?, ?, ?)",
                           "INSERT_ACTIVITY": "INSERT INTO activities('sport_id', 'user_id', 'time', 'distance') "
                                              "VALUES (?, ?, ?, ?)",
                           "INSERT_SPORT": "INSERT INTO sports('name', 'moving') VALUES (?, ?)",
                           "DELETE": "TODO",
                           "FETCH": "SELECT ? FROM ? WHERE ?=?",
                           "FETCH_ALL": "SELECT * FROM ?"}

    def create_connection(self) -> Connection:
        # TODO: error handling
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

    def insert_activity(self, *, sport_id: int, user_id: int, time: int, distance: int = 0):
        self._execute("INSERT_ACTIVITY", sport_id, user_id, time, distance)

    def insert_moving_activity(self, *, sport_id: int, user_id: int, time: int, distance: int):
        self.insert_activity(sport_id=sport_id, user_id=user_id, time=time, distance=distance)
