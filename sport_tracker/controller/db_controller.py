from datetime import date
from os.path import dirname
from sqlite3 import Connection, connect, IntegrityError, Cursor, Error as SQLError
from typing import Any

import sport_tracker
from sport_tracker.common.exceptions import InvalidArgumentError
from sport_tracker.logger import logger
from sport_tracker.model.person import ActivityLevel


class DBController:
    def __init__(self):
        self.db_file: str = f"{dirname(sport_tracker.__file__)}/model/database.db"  # db file is auto-created
        self.connection: Connection
        self.statements = {"UPDATE_USER": "UPDATE users SET 'name'=?, 'born_date'=?, 'weight'=?, 'height'=?, "
                                          "'gender'=?, 'activity_level'=? WHERE id=?",
                           "UPDATE_SPORT": "UPDATE sports SET 'name'=?, 'moving'=? WHERE id=?",
                           "UPDATE_ACTIVITY": "UPDATE activities SET 'sport_id'=?, 'user_id'=?, 'time'=?, "
                                              "'distance'=? WHERE id=?",
                           "INSERT_USER": "INSERT INTO users('name', 'born_date', 'weight', 'height', 'gender',"
                                          " 'activity_level') "
                                          "VALUES (?, ?, ?, ?, ?, ?);",
                           "INSERT_ACTIVITY": "INSERT INTO activities('sport_id', 'user_id', 'time', 'distance') "
                                              "VALUES (?, ?, ?, ?);",
                           "INSERT_SPORT": "INSERT INTO sports('name', 'moving') VALUES (?, ?);",
                           # table names cannot be parametrized, thus separate delete statements
                           "DELETE_USER": "DELETE FROM users WHERE id=?",
                           "DELETE_ACTIVITY": "DELETE FROM activities WHERE id=?",
                           "DELETE_SPORT": "DELETE FROM sports WHERE id=?",
                           # table names cannot be parametrized, thus separate fetch statements
                           "FETCH_ALL_USERS": "SELECT id, name, born_date, weight, height, "
                                              "CASE WHEN gender = 0 then 'male' else 'female' END, activity_level"
                                              " FROM users LIMIT ?;",
                           "FETCH_USER_BY_ID": "SELECT name, born_date, weight, height, "
                                               "CASE WHEN gender = 0 then 'male' else 'female' END, "
                                               "activity_level FROM users WHERE id=?;",
                           "FETCH_ALL_ACTIVITIES": "SELECT * FROM activities LIMIT ?;",
                           "FETCH_ALL_SPORTS": "SELECT id, name, CASE WHEN moving = 1 then 'yes' else 'no' END "
                                               "FROM sports LIMIT ?;",
                           # table names cannot be parametrized, thus separate fetch row id statements
                           "FETCH_ROW_ID_USERS": "SELECT ROWID FROM users WHERE name=?;",
                           "FETCH_ROW_ID_SPORTS": "SELECT ROWID FROM sports WHERE name=?;",
                           }

    def create_connection(self) -> Connection:
        """
        Creates connection to the database file
        :return: established connection
        """
        try:
            return connect(self.db_file)
        except SQLError as e:
            logger.error(str(e))
            exit(1)

    def __enter__(self):
        self.connection = self.create_connection()
        self._populate_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        if exc_val:
            raise

    def _execute(self, statement: str, *args) -> Cursor:
        """
        Executes statement from :statements: dictionary with given parameters
        :param statement: statement from :statements" dictionary to be executed
        :param args:
        :return: cursor from the connection
        """
        if statement not in self.statements:
            raise InvalidArgumentError(f"statement argument must be one of the {self.statements.keys()}")
        c = self.connection.cursor()
        try:
            c.execute(self.statements[statement], args)
        except IntegrityError:
            raise
        except SQLError as e:
            logger.error(str(e))
            self.connection.close()
            raise
        else:
            self.connection.commit()
            return c

    # initial population
    def _populate_db(self):
        with open(f"{dirname(sport_tracker.__file__)}/common/create_tables.sql") as create_tables_sql:
            try:
                tables_creation_statements = create_tables_sql.read()
                for single_table_creation_statement in tables_creation_statements.split(";"):
                    self.connection.execute(single_table_creation_statement)
                self.connection.commit()
            except (FileNotFoundError, SQLError) as e:
                logger.error(str(e))
                raise

    # public insert methods
    def insert_user(self, *, name: str, date_born: date, weight: float, height: int, gender: int,
                    activity: ActivityLevel) -> bool:
        """
        Method inserts new user into database
        :param name: User's name
        :param date_born: date of birth
        :param weight: weight of the user in kg's
        :param height: height of the user in cm's
        :param gender: user's gender, 0 for male, 1 for female
        :param activity: level of activity (see Person class file)
        :return: True if operation was successful, False otherwise
        :raise: error different than IntegrityError which is handled
        """
        try:
            self._execute("INSERT_USER", name, date_born.strftime("%Y-%m-%d"), weight, height, gender, activity.value)
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

    # public delete methods
    def delete_user(self, *, row_id: int):
        # TODO: Implement
        pass

    def delete_activity(self, *, row_id: int):
        # TODO: Implement
        pass

    def delete_sport(self, *, row_id: int):
        # TODO: Implement
        pass

    # fetch methods
    def fetch_row_id(self, *, table: str, column: str = 'name', value: Any) -> int:
        result_cursor: Cursor = self._execute(f"FETCH_ROW_ID_{table.upper()}", value)
        result_list: list = result_cursor.fetchall()
        if not len(result_list):
            raise IntegrityError(f"No value for '{value}' in column '{column}' of table '{table}' found!")
        if len(result_list) == 1:
            return result_list[0][0]
        else:
            raise IntegrityError(f"Multiple values for '{value}' in column '{column}' of table '{table}' found!")

    def fetch_all(self, *, table: str, limit: int = 50) -> list:
        result_cursor: Cursor = self._execute(f"FETCH_ALL_{table.upper()}", limit)
        return result_cursor.fetchall()

    def fetch_user_by_id(self, *, row_id: int) -> list:
        result_cursor: Cursor = self._execute("FETCH_USER_BY_ID", row_id)
        return result_cursor.fetchall()

    # update methods
    def update_user(self, *, name: str, date_born: date, weight: float, height: int, gender: int,
                    activity: ActivityLevel, id_to_modify: int) -> bool:
        self._execute("UPDATE_USER", name, date_born.strftime("%Y-%m-%d"), weight, height, gender,
                      activity.value, id_to_modify)
        return True

    def update_sport(self, *, name: str, moving: bool, id_to_modify: int) -> bool:
        self._execute("UPDATE_SPORT", name, 1 if moving else 0, id_to_modify)
        return True

    def update_activity(self, *, sport_id: int, user_id: int, time: int, distance: int = 0, id_to_modify: int) -> bool:
        self._execute("UPDATE_ACTIVITY", sport_id, user_id, time, distance, id_to_modify)
        return True
