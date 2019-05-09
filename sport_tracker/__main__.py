from sport_tracker.argparser import init_args
from sport_tracker.controller.argument_actions import process_args


def main():
    process_args(init_args())
 
    
if __name__ == '__main__':
    main()

