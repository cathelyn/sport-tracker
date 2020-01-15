from sport_tracker.controller.user_actions import UserActions

def process_args(arguments):
    actions_dict : dict = {
        'add-user': UserActions.add_user,
        'modify-user': UserActions.modify_user,
        'list-users': UserActions.list_users,
        'delete-user': None,  #TODO: Implement
        'export-users': None,
        'add-activity': None,
        'list-activities': None,
        'modify-activity': None,
        'delete-activity': None,
        'export-activities': None
    }

    actions_dict[arguments.action[0]](*arguments.parameters)
