from datetime import date
from math import floor

from pint import UnitRegistry
from pint.errors import UndefinedUnitError, DimensionalityError

from sport_tracker.common.exceptions import InvalidArgumentError
from sport_tracker.controller.db_controller import DBController
from sport_tracker.logger import logger
from sport_tracker.model.person import ActivityLevel
from sport_tracker.view.terminal_output import TerminalOutput


class UserActions:
    @staticmethod
    def _obtain_user_info(default_values: dict = None):
        unit_registry = UnitRegistry()
        # name input
        while True:
            default_prompt = f" [{default_values['user_name']}]" if default_values else ''
            user_name: str = input(f"Input your name{default_prompt}: ")
            if user_name:
                break
            elif default_values:
                user_name = default_values['user_name']
                break
            else:
                logger.error("User's name cannot be empty")
        # birth date input
        while True:
            default_prompt = f" [{default_values['date_of_birth']}]" if default_values else ''
            date_of_birth: str = input(f"Input your birth date in format DD-MM-YYYY{default_prompt}: ")
            if not date_of_birth and default_values:
                date_of_birth = f"{default_values['date_of_birth'].split('-')[2]}-" \
                    f"{default_values['date_of_birth'].split('-')[1]}-" \
                    f"{default_values['date_of_birth'].split('-')[0]}"
            try:
                # TODO: Investigate this handling in comparison with name handling
                date_of_birth: date = date(day=int(date_of_birth.split("-")[0]),
                                           month=int(date_of_birth.split("-")[1]),
                                           year=int(date_of_birth.split("-")[2]))
                if not date_of_birth:
                    raise ValueError("Empty date")
            except (TypeError, IndexError):
                logger.error("Incorrect date format, try again")
            except ValueError:
                logger.error("Impossible date, try again")
            else:
                break
        # weight input
        while True:
            default_prompt = f" [{default_values['weight']}] kg" if default_values else ''
            weight: str = input(f"Enter your weight with units designation{default_prompt}: ")
            try:
                if not weight and default_values:
                    weight = f"{default_values['weight']} kg"
                elif not weight:
                    raise UndefinedUnitError
                weight: float = unit_registry.Quantity(weight).to(unit_registry.kilogram).magnitude
            except (UndefinedUnitError, DimensionalityError) as e:
                logger.error(str(e))
            else:
                break
        # height input
        while True:
            default_prompt = f" [{default_values['height']}] cm" if default_values else ''
            height: str = input(f"Enter your height with unit designation{default_prompt}: ")
            try:
                if not height and default_values:
                    height = f"{default_values['height']} cm"
                if not height:
                    raise UndefinedUnitError
                height: int = floor(unit_registry.Quantity(height).to(unit_registry.centimeter).magnitude)
            except (UndefinedUnitError, DimensionalityError) as e:
                logger.error(str(e))
            else:
                break
        # gender input
        while True:
            default_prompt = f" [{default_values['gender']}]" if default_values else ''
            gender: str = input(f"Enter your gender [male/female]{default_prompt}: ")
            if not gender and default_values:
                gender = default_values['gender']
                break
            if gender.lower().startswith("m"):
                gender: int = 0  # male is stored as 0 in db
                break
            elif gender.lower().startswith("f"):
                gender: int = 1  # female is stored as 1 in db
                break
            else:
                logger.error("Incorrect gender, use either male or female")
        # activity level input
        while True:
            default_prompt = f" [{default_values['activity_level']}]" if default_values else ''
            activity_level: str = input(f"Enter your activity level "
                                        f"[1 = sedentary to 4 = professional athlete]{default_prompt}: ")
            try:
                if not activity_level and default_values:
                    activity_level = default_values['activity_level']
                if not activity_level:
                    raise InvalidArgumentError
                activity_level: int = int(activity_level)
            except \
                    (TypeError, InvalidArgumentError):
                logger.error("Incorrect activity level, try again")
            else:
                if 1 <= activity_level <= 4:
                    break
                else:
                    logger.error("Activity level must be either 1, 2, 3 or 4")
        return user_name, date_of_birth, weight, height, gender, activity_level

    @staticmethod
    def create_user():
        unit_registry = UnitRegistry()
        while True:
            logger.info("Registering new user")
            user_name, date_of_birth, weight, height, gender, activity_level = UserActions._obtain_user_info()
            # print information for user to verify
            print("\nVerify these information: ")
            print(f"Name: {user_name}")
            print(f"Age: {floor((date.today() - date_of_birth).total_seconds() / 365 / 24 / 3600)} years")
            print(f"Weight: {weight * unit_registry.kilogram}")
            print(f"Height: {height * unit_registry.centimeter}")
            print(f"Gender: {'male' if gender == 0 else 'female'}")
            print(f"Activity level: {ActivityLevel(activity_level)}")

            while True:
                choice = input("Is this correct? [Y/n]: ") or "y"
                if choice.lower().startswith("y"):
                    correct = True
                    break
                elif choice.lower().startswith("n"):
                    correct = False
                    break

            if correct:
                break

        # insert obtained pieces of information into database
        with DBController() as db:
            db.insert_user(name=user_name, date_born=date_of_birth, weight=weight,
                           height=height, gender=gender, activity=ActivityLevel(activity_level))
            logger.info("User added")
            print(f"User {user_name} added successfully.")

    @staticmethod
    def list_users():
        with DBController() as db:
            TerminalOutput.print_table(header=['ID', 'Name', 'Birth date', 'Weight', 'Height',
                                               'Gender', 'Activity Level'],
                                       data=db.fetch_all(table="users"))

    @staticmethod
    def modify_user():
        logger.info("Modifying user")
        print("Choose what user to modify: ")
        UserActions.list_users()
        while True:
            id_to_modify: str = input("ID of user to modify: ")
            try:
                with DBController() as db:
                    number_of_users: int = len(db.fetch_all(table="users"))
                id_to_modify: int = int(id_to_modify)
                if 1 <= id_to_modify <= number_of_users:
                    break
                else:
                    raise InvalidArgumentError(f"User id must be in range 1 - {number_of_users}")
            except (TypeError, InvalidArgumentError):
                logger.error("Incorrect choice, try again")

        logger.info("Obtaining all the pieces of information about edited ")
        with DBController() as db:
            fetched_info: list = db.fetch_user_by_id(row_id=id_to_modify)[0]
            fields: list = ['user_name', 'date_of_birth', 'weight', 'height', 'gender', 'activity_level']
            default_info: dict = {field: info for field, info in zip(fields, fetched_info)}

        logger.info("Obtaining new info")
        user_name, date_of_birth, weight, height, gender, activity_level = UserActions._obtain_user_info(
            default_values=default_info)

        with DBController() as db:
            db.update_user(name=user_name, date_born=date_of_birth, weight=weight,
                           height=height, gender=gender, activity=ActivityLevel(activity_level),
                           id_to_modify=id_to_modify)
        logger.info("Update: success")
        print("User was updated successfully.")

    @staticmethod
    def delete_user():
        raise NotImplementedError

    @staticmethod
    def export_users():
        raise NotImplementedError
