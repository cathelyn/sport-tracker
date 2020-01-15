from argparse import ArgumentParser

arg_parser = ArgumentParser()

user_actions = ['create-user',
                'modify-user',
                'list-users',
                'delete-user',
                'export-users']

activity_actions = ['add-activity',
                    'list-activities',
                    'modify-activity',
                    'delete-activity',
                    'export-activities']

sport_actions = ['add-sport',
                 'list-sports',
                 'modify-sports',
                 'delete-sport']

arg_parser.add_argument("action",
                        nargs=1,
                        help="SportTracker action",
                        choices=user_actions + activity_actions + sport_actions)
arg_parser.add_argument("parameters",
                        nargs="*",
                        help="Parameters of specified action")
arg_parser.add_argument("--no_confirm",
                        help="Disable confirmation dialogs",
                        action="store_true",
                        default=False)


def init_args():
    return arg_parser.parse_args()
