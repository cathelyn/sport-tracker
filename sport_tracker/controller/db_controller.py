from datetime import date
from os.path import dirname
from sqlite3 import Connection, connect, IntegrityError, Error

import sport_tracker
from sport_tracker.common.exceptions import IllegalArgumentException
from sport_tracker.logger import logger
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
        """
        Creates connection to the database file
        :return: established connection
        """
        try:
            return connect(self.db_file)
        except Error as e:
            logger.error(str(e))
            exit(1)

    def _execute(self, statement: str, *args):
        """
        Executes statement from :statements: dictionary with given parameters
        :param statement: statement from :statements" dictionary to be executed
        :param args:
        :return:
        """
        if statement not in self.statements:
            raise IllegalArgumentException(f"statement argument must be one of the {self.statements.keys()}")
        c = self.connection.cursor()
        try:
            c.execute(self.statements[statement], args)
        except IntegrityError:
            raise
        except Error as e:
            logger.error(str(e))
            exit(1)
        else:
            self.connection.commit()
        finally:
            self.connection.close()

    # public insert methods
    def insert_user(self, *, name: str, date_born: date, weight: float, height: int, activity: ActivityLevel) -> bool:
        """
        Method inserts new user into database
        :param name: User's name
        :param date_born: date of birth
        :param weight: weight of the user in kg's
        :param height: height of the user in cm's
        :param activity: level of activity (see Person class file)
        :return: True if operation was successful, False otherwise
        :raise: error different than IntegrityError which is handled
        """
        try:
            self._execute("INSERT_USER", name, date_born.strftime("%Y-%m-%d"), weight, height, activity.value)
        except IntegrityError as e:
            if "name" in str(e):
                logger.error("User's name already exists in the database")
                return False
            else:
                raise
        else:
            return True

    def insert_activity(self, *, sport_id: int, user_id: int, time: int, distance: int = 0) -> bool:
        """
        Method inserts new general activity into database
        :param sport_id: rowid of the sport from :sports: table
        :param user_id: rowid of the user from :users: table
        :param time: total time spent by doing this activity
        :param distance: total distance done doing this activity, defaults to zero for static activity
        :return: True if the operation was completed successfully
:       """
        self._execute("INSERT_ACTIVITY", sport_id, user_id, time, distance)
        return True

    def insert_moving_activity(self, *, sport_id: int, user_id: int, time: int, distance: int) -> bool:
        """
        Method inserts new moving activity into database
        :param sport_id: rowid of the sport from :sports: table
        :param user_id: rowid of the user from :users: table
        :param time: total time spent by doing this activity
        :param distance: total distance done doing this activity
        :return: True if the operation was completed successfully
        """
        self.insert_activity(sport_id=sport_id, user_id=user_id, time=time, distance=distance)
        return True

    def insert_sport(self, *, name: str, moving: bool) -> bool:
        """
        Method inserts new sport into database
        :param name: name of the sport to be inserted
        :param moving: boolean: designates moving, i.e. distance based sport
        :return: True if operation was successful, False otherwise
        :raise: error different than IntegrityError which is handled
        """
        try:
            self._execute("INSERT_SPORT", name, 1 if moving else 0)
        except IntegrityError as e:
            if 'name' in str(e):
                logger.error(f"Sport named {name} already exists in the database")
            else:
                raise
        else:
            return True


if __name__ == '__main__':
    db = DBController()
    db.insert_sport(name="Sprint", moving=True)

