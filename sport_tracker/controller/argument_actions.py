from sport_tracker.controller.user_actions import UserActions
from sport_tracker.controller.activity_actions import ActivityAction
from sport_tracker.controller.sport_actions import SportAction

def process_args(arguments):
    actions_dict : dict = {
        'create-user': UserActions.create_user,
        'modify-user': UserActions.modify_user,
        'list-users': UserActions.list_users,
        'delete-user': UserActions.delete_user,
        'export-users': UserActions.export_users,
        'add-activity': ActivityAction.add_activity,
        'create-activity': ActivityAction.create_activity,
        'list-activities': ActivityAction.list_activities,
        'modify-activity': ActivityAction.modify_activity,
        'delete-activity': ActivityAction.delete_activity,
        'export-activities': ActivityAction.export_activities,
        'add-sport': SportAction.add_sport,
        'list-sports': SportAction.list_sports,
        'modify-sports': SportAction.modify_sport,
        'delete-sport': SportAction.delete_sport
    }

    # as arguments are checked by argparser, it's safe to execute args without
    # other checks
    actions_dict[arguments.action[0]](*arguments.parameters)
