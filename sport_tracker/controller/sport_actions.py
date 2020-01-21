from sport_tracker.controller.db_controller import DBController
from sport_tracker.logger import logger
from sport_tracker.view.terminal_output import TerminalOutput


class SportAction:
    @staticmethod
    def _obtain_sport_info(default_values: dict = None) -> (str, int):
        while True:
            # name input
            default_prompt = f" [{default_values['sport_name']}]" if default_values else ''
            sport_name: str = input(f"Input sport's name{default_prompt}: ")
            if sport_name:
                break
            if not sport_name and default_values:
                sport_name = default_values['sport_name']
                break
            else:
                logger.error("Sport's name cannot be empty")
        # moving input
        while True:
            default_prompt = f" [{default_values['moving']}]" if default_values else ''
            moving: str = input(f"Is this sport distance based (moving) {default_prompt}? ")
            if not moving and default_values:
                moving: int = default_values['moving']
                break
            if moving.lower().startswith('y'):
                moving: int = 1
                break
            elif moving.lower().startswith('n'):
                moving: int = 0
                break
            else:
                logger.error("Incorrect value, must be either yes or no")

        return sport_name, moving

    @staticmethod
    def add_sport():
        while True:
            logger.info("Registering new sport")
            sport_name, moving = SportAction._obtain_sport_info()
            # print information for user to verify
            print("\nVerify these information: ")
            print(f"Name of the sport: {sport_name}")
            print(f"Sport is distance based (moving): {'yes' if moving == 1 else 'no'}")
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
            db.insert_sport(name=sport_name, moving=moving==1)
            logger.info("Sport added")
            print(f"Sport {sport_name} added successfully.")

    @staticmethod
    def modify_sport():
        raise NotImplementedError

    @staticmethod
    def list_sports():
        with DBController() as db:
            TerminalOutput.print_table(header=['ID', 'Name', 'Distance based?'],
                                       data=db.fetch_all(table="sports"))

    @staticmethod
    def delete_sport():
        raise NotImplementedError