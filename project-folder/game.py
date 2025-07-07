from js import printToScreen

def handle_input(user_input):
    printToScreen(f"> {user_input}")
    # TODO: Parse input and update game state

game_state = GameState()
buffer = []
current_phase = "menu"
menu_step = "prompt"  # Tracks which part of the menu we're on


def flush_buffer():
    from js import printToScreen
    for line in buffer:
        printToScreen(line)




# Important game functions
def handle_input(user_input):
    global buffer, current_phase, menu_step

    buffer.clear()

    if current_phase == "menu":
        if menu_step == "prompt":
            buffer.append("------- Whittershok -------")
            buffer.append(".-.-.-.-.-.-.-.-.-.-.-..-.-.")
            buffer.append("Game Menu")
            buffer.append("1. Create New Game")
            buffer.append("2. Load Game")
            buffer.append("3. Exit")
            buffer.append("Select an option:")
            menu_step = "await_choice"

        elif menu_step == "await_choice":
            if user_input == "1":
                game_state.create_new()  # You'll need to refactor this too
                buffer.append("New game started.")
                current_phase = "play"
                menu_step = "prompt"
            elif user_input == "2":
                buffer.append("Enter save slot (1-3):")
                menu_step = "await_slot"
            elif user_input == "3":
                buffer.append("Goodbye!")
                current_phase = "exit"
            else:
                buffer.append("Invalid choice. Try again.")
                menu_step = "prompt"

        elif menu_step == "await_slot":
            try:
                slot = int(user_input)
                game_state.load_from_slot(slot)
                buffer.append(f"Loaded save slot {slot}.")
                current_phase = "play"
                menu_step = "prompt"
            except ValueError:
                buffer.append("Invalid slot. Enter a number between 1 and 3.")
                menu_step = "prompt"

    flush_buffer()


setup_step = None


