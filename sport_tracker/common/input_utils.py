def confirm_validity() -> bool:
    while True:
        choice = input("Is this correct? [Y/n]: ") or "y"
        if choice.lower().startswith("y"):
            return True
        elif choice.lower().startswith("n"):
            return False
