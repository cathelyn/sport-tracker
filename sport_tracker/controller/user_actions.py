from datetime import date
from math import floor

from pint import UnitRegistry
from pint.errors import UndefinedUnitError, DimensionalityError

from sport_tracker.controller.db_controller import DBController
from sport_tracker.logger import logger
from sport_tracker.model.person import ActivityLevel


class UserActions:
    @staticmethod
    def add_user():
        while True:
            logger.info("Registering new user")
            unit_registry = UnitRegistry()
            user_name: str = input("Input your name: ")
            # birth date input
            while True:
                date_of_birth: str = input("Input your birth date in format DD-MM-YYYY: ")
                try:
                    date_of_birth: date = date(day=int(date_of_birth.split("-")[0]),
                                               month=int(date_of_birth.split("-")[1]),
                                               year=int(date_of_birth.split("-")[2]))
                except (TypeError, IndexError):
                    logger.error("Incorrect date format, try again")
                except ValueError:
                    logger.error("Impossible date, try again")
                else:
                    break
            # weight input
            while True:
                weight: str = input("Enter your weight with units designation [kg]: ")
                try:
                    weight: float = unit_registry.Quantity(weight).to(unit_registry.kilogram).magnitude
                except (UndefinedUnitError, DimensionalityError) as e:
                    logger.error(str(e))
                else:
                    break
            # height input
            while True:
                height: str = input("Enter your height with unit designation [cm]: ")
                try:
                    height: int = floor(unit_registry.Quantity(height).to(unit_registry.centimeter).magnitude)
                except (UndefinedUnitError, DimensionalityError) as e:
                    logger.error(str(e))
                else:
                    break
            # gender input
            while True:
                gender: str = input("Enter your gender [male/female]: ")
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
                activity_level: str = input("Enter your activity level [1 = sedentary to 4 = professional athlete]: ")
                try:
                    activity_level: int = int(activity_level)
                except TypeError:
                    logger.error("Incorrect activity level, try again")
                else:
                    if 1 <= activity_level <= 4:
                        break
                    else:
                        logger.error("Activity level must be either 1, 2, 3 or 4")
            # print information for user to verify
            print("\nVerify these information: ")
            print(f"Name: {user_name}")
            print(f"Age: {floor((date.today() - date_of_birth).total_seconds() / 365 / 24 / 3600)}")
            print(f"Weight: {weight}")
            print(f"Height: {height}")
            print(f"Gender: {'male' if gender == 0 else 'female'}")
            print(f"Activity level: {activity_level}")

            while True:
                choice = input("Is this correct? [y]: ") or "y"
                if choice.lower().startswith("y"):
                    correct = True
                    break
                elif choice.lower().startswith("n"):
                    correct = False
                    break

            if correct:
                break

        with DBController() as db:
            db.insert_user(name=user_name, date_born=date_of_birth, weight=weight,
                           height=height, gender=gender, activity=ActivityLevel(activity_level))

    @staticmethod
    def add_sport(self):
        # TODO: Implement
        pass
