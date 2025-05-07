import json
import os
import re
import time

# SET CONSTANTS
SPEED = 0.02 # The smaller the faster
FOLDER_PATH = "C:/Users/Aaron/python_files/video_games/whittershok/game_saves"
os.makedirs(FOLDER_PATH, exist_ok=True)


# Special Semantics for Terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear') #Clears on both Windows and Mac


class GameState:
    def __init__(self):
        self.name = ""
        self.health = 100
        self.gold = 0
        self.quest_log = []
        self.inventory = []
        self.location = ""
        self.shop_inventory = {}
        self.world_state = {}

    def create_new(self):
        self.name = input("Enter character name: ")
        self.health = 100
        self.gold = 0
        self.quest_log = []
        self.inventory = []
        self.location = "prelude"
        self.shop_inventory = {"Bug Net": 5, "Sword": 10, "Apple Pie": 3, "Broken Dagger": 7}
        self.world_state = {
        "Town Center": {
            "visited": False,
        },
        "Bazaar": {
            "visited": False,
        },
        "The Croftward": {
            "visited": False,
            "staff": False,
        },
        "Eastern Orchard": {
            "visited": False,
            "bennyboy": False,
        },
        "Windshire Chapels": {
            "visited": False,
            "fliers": False
        },
        "Forest Entrance": {
            "visited": False,
            "witch_defeated": False
        },
        "Abandoned Witch Hut":{
            "visited": False,
        },
        "Twilight Grove":{
            "visited": False,
            "fountain": False},}

    def save_to_slot(self, slot):
        file_path = self._get_file_path(slot)

        data = {
            "name": self.name,
            "health": self.health,
            "gold": self.gold,
            "quest_log": self.quest_log,
            "inventory": self.inventory,
            "shop_inventory": self.shop_inventory,
            "location": self.location,
            "world_state": self.world_state,
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Game saved to slot {slot}.")

    def load_from_slot(self, slot):
        file_path = self._get_file_path(slot)

        if not os.path.exists(file_path):
            print(f"No save file found in slot {slot}.")
            return False

        with open(file_path, "r") as f:
            data = json.load(f)

        self.name = data.get("name", "")
        self.health = data.get("health", 0) 
        self.gold = data.get("gold", 0)
        self.quest_log = data.get("quest_log", [])
        self.inventory = data.get("inventory", [])
        self.shop_inventory = data.get("shop_inventory", {})
        self.location = data.get("location", "")
        self.world_state = data.get("world_state", {})

        print(f"Game loading from slot {slot}.")
        time.sleep(2)
        return True
        
    def _get_file_path(self, slot):
        filenames = {
            1: "save_slot_one.json",
            2: "save_slot_two.json",
            3: "save_slot_three.json"
        }
        return os.path.join(FOLDER_PATH, filenames.get(slot, "invalid_slot.json"))

    def show_state(self): #Not used
        print("\nCurrent Game State:")
        print("Name:", self.name)
        print("Health:", self.health)
        print("Location:", self.location)
        print("Inventory:", self.inventory)
        print("Quest Log:", self.quest_log)
        print()


    # Dictionary to pull and update variables within CLASS
    # Getter for name
    def get_name(self):
        return self.name
    
    # Getter for health
    def get_health(self):
        return self.health
    
    # Setter for health
    def set_health(self, new_health):
        self.health = new_health

    # Getter for gold
    def get_gold(self):
        return self.gold
    
    # Setter for gold
    def set_gold(self, new_amount):
        self.gold = new_amount

    # Setter for shop inventory
    def get_shop_inventory(self):
        return self.shop_inventory
    
    # Getter for shop inventory
    def set_shop_inventory(self, new_inventory):
        self.shop_inventory = new_inventory
    
    # Getter for inventory
    def get_inventory(self):
        return self.inventory
    
    # Remover from inventory
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    # Adder to inventory
    def add_to_inventory(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    # Getter for location
    def get_location(self):
        return self.location

    # Setter for location
    def set_location(self, new_location):
        self.location = new_location
    
    # __________QUEST FUNCTIONS_______________
    # Getter for quest_log
    def get_quest_log(self):
        return self.quest_log

    # Check quest status (returns false in not active)
    def is_quest_active(self, title):
        for quest in self.quest_log:
            if quest["title"] == title:
                return quest["status"].lower() == "active"
        return False
    
    # Check to see if quest is completed (returns false if not complete)
    def is_quest_completed(self, title):
        for quest in self.quest_log:
            if quest["title"] == title:
                return quest["status"].lower() == "completed"
        return False
    
    # Complete quest
    def complete_quest(self, title):
        for quest in self.quest_log:
            if quest["title"] == title:
                quest["status"] = "Completed"

    # Adder to quest_log
    def add_quest(self, quest_dict):
        self.quest_log.append(quest_dict)


    # Getter for world_state
    def get_world_state(self):
        return self.world_state

    # Setter for world_state
    def set_world_state(self, new_world_state):
        self.world_state = new_world_state


    def shop_menu(self):
        shop_items = {
        "Bug Net": 10,
        "Sword": 25,
        "Apple Pie": 5,
        "Broken Dagger": 15
    }

    def scroll_typewriter(self, text):
        # Dictionary to handle substitutions like player name
        substitutions = {
            "name": self.name
        }

        # Perform the substitutions (e.g., replace [name] with self.name)
        for key, value in substitutions.items():
            text = text.replace(f"[{key}]", str(value))

        i = 0
        while i < len(text):
            if text[i:i+7] == "[pause]":  # Detect "[pause]" and introduce a pause
                time.sleep(1)  # Adjust the pause time as needed
                i += 7  # Skip past the "[pause]" tag
                continue

            print(text[i], end='', flush=True)
            time.sleep(SPEED)  # Adjust the speed of typing as needed
            i += 1

# Important game loop functions
def run_game_title_menu(state):
    print("\n------- Whittershok -------")
    print(".-.-.-.-.-.-.-.-.-.-.-..-.-.-.-.")
    print("Game Menu")
    print("1. Create New Game")
    print("2. Load Game")
    print("3. Save Game")
    print("4. Exit")
    choice = input("Select an option: ")

    if choice == "1":
        state.create_new()
    elif choice == "2":
        slot = int(input("Enter save slot (1-3): "))
        state.load_from_slot(slot)
    elif choice == "3":
        slot = int(input("Enter save slot (1-3): "))
        state.save_to_slot(slot)
    elif choice == "4":
        run = False
    else:
        print("Invalid choice. Try again.")

def show_inventory(state):
    inventory = state.get_inventory()
    print("\n--- Inventory ---")
    if not inventory:
        print("Your inventory is empty.")
    else:
        for item in inventory:
            print(f"- {item}")
    print("-----------------\n")
    input("Press Enter to continue...")

def show_quest_log(state):
    clear()
    print("--- Quest Log ---\n")
    quests = state.get_quest_log()

    if not quests:
        print("You have no quests right now.")
    else:
        for idx, quest in enumerate(quests, start=1):
            print(f"{idx}. {quest['title']}")
            print(f"   Status: {quest['status']}")
            print(f"   Description: {quest['description']}")
            

    input("Press Enter to return...")

def prompt_player_action(state, allowed_directions=None):
    if allowed_directions is None:
        allowed_directions = {"north", "south", "east", "west"}

    while True:
        time.sleep(1)
        clear()
        location = state.get_location()
        formatted_location = location.replace("_", " ").title()
        print(f"\nLocation: {formatted_location}\n\n")

        print("Which direction do you go? (north, south, east, west)")
        print(f"HP: {state.health}     Gold: {state.get_gold()}     (I) Inventory   (Q) Quest Log   (S) Save Game   (E) Exit Game")
        action = input("ACTION: ").strip().lower()

        if action in allowed_directions:
            return action

        elif action == "i":
            show_inventory(state)
            clear()

        elif action == "q":
            show_quest_log(state)
            clear()

        elif action == "s":
            slot = int(input("Enter save slot (1-3): "))
            state.save_to_slot(slot)
            print("Game saved.")
            time.sleep(1)
            clear()

        elif action == "e":
            confirm = input("Are you sure you want to quit? (y/n): ").strip().lower()
            if confirm == "y":
                run_game_title_menu(state)
                
            else:
                clear()

        else:
            print("You can't go that way. Try again.")
            time.sleep(1)
            clear()



# Combat encounters
def witch_combat(state):
    name = state.get_name
    player_health = state.get_health()
    witch_health = 150
    attacks_per_turn = 2 # Modify this so that it can change if you consume something....
    allowed_actions = []
    turns = ["Witch", "Player", "Tannenbark"]
    has_sword = "Sword" in state.get_inventory()
    if has_sword:
        allowed_actions.append("(S) Sword")
    has_broken_dagger = "Broken Dagger" in state.get_inventory()
    if has_broken_dagger:
        allowed_actions.append("(B) Broken Dagger")
    
    allowed_actions.append("(F) Fists") # Default attack

    has_health_potion = "Health Potion" in state.get_inventory()
    if has_health_potion:
        allowed_actions.append("(H) Health Potion")
    has_apple_pie = "Apple Pie" in state.get_inventory()
    if has_apple_pie:
        allowed_actions.append("(A) Apple Pie")
    
    
    run = True
    round = 1
    while run:
        

        
        
        for name in turns:
            if name == "Witch": # The Witch's Turn
                time.sleep(1)
                clear()
                print(f"Round: {round}")
                print("It is the Wicked Hag's turn")
                time.sleep(1)
                if round == 1:
                    witch_text = "Witch Dialogue One "
                elif round == 2:
                    witch_text = "Witch Dialogue Two"
                elif round == 3:
                    witch_text = "Witch Dialogue Three"
                else:
                    witch_text = "Default Witch Dialogue for if the fight extends super long"
                state.scroll_typewriter(witch_text)

            elif name == "Player": # The Player's Turn
                if attacks_per_turn == 0:
                    break
                else:
                    attack = True
                while attack:
                    time.sleep(1)
                    clear()
                    print(f"Round: {round}")
                    print(f"It is {name}'s turn")
                    time.sleep(1)
                    if attacks_per_turn <= 1:
                        print("You have one attack left")
                    else:
                        print(f"You have {attacks_per_turn} attacks left.")
                    
                    print("\n\n\n")
                    
                    print(f"HP: {state.health}    " + "    ".join(allowed_actions))  # Print combat options 4 spaces between each item
                    action = input("ACTION: ").strip().lower()
                    clear()
                    if action == "s" and has_sword:
                        print("You use your sword!")
                        state.scroll_typewriter("""[name]
Eat lead, you creepy person!""")
                        damage = 100
                    elif action == "b" and has_sword:
                        print("You use your broken dagger!")
                        state.scroll_typewriter("""[name]
Take that you wicked hag!""")
                        damage = 50
                    elif action == "f":
                        print("You use your fists to pummel the hag!")
                        state.scroll_typewriter("Fist d") 

                    else:
                        print("Invalid entry. Please try again.")
                    time.sleep(1)
                    print(f"You deal {damage} damage")
            else: # Tannenbark's Turn
                pass
            round += 1

# Areas
def prelude(state):
    print("Prelude\n\n")
    intro_text = """[pause]You wake up to sunlight in your eyes, which is easily the most attention you’ve received all week.
You lie in bed, wide awake and wondering whether that weird letter from the town wizard was just another prank—or worse, real.
[pause]
You read the letter:
Dear [name],
Meet me at the town center at noon.
I need a favor. Please arrive in a timely manner.

Your wizard,
Elvis 

(P.S. Don't tell anyone I contacted you. Also, bring a spoon.)

[pause]
It’s strange. Wizards are usually too busy muttering at scrolls or accidentally exploding sheep to ask favors of others—especially from someone as aggressively average as you.

You’re not strong. You’re not clever. People don’t dislike you—they just don’t often remember you exist. You’re also, notably, the reigning loser of Apple Cart Racing—a children’s game. Played by actual children.

But never mind all that. Your backstory is short, your socks don’t match, and destiny apparently doesn’t care.

[pause]"""
    
    state.scroll_typewriter(intro_text)
    
    _ = input("\n\nPress ENTER to continue")
    
def town_center(state):
    # Set Flags
    world_state = state.get_world_state()
    location_state = world_state.get("Town Center", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_fliers = "Earl's Fliers" in state.get_inventory()

    if "Return The Wizard Staff" not in quest_titles:
        state.add_quest({
            "title": "Return The Wizard Staff",
            "description": "Elvis the wizard needs his Staff, stolen by the Old Hag, to seal the Mystic Gate.",
            "status": "Active"
        })

    clear()
    print(f"Location: Town Center\n\n")
    if not location_state.get("visited", False):
        state.scroll_typewriter("You step into the Town Center for the first time. The wizard needs his staff! The old witch stole it.")
        location_state["visited"] = True  # Update visited flag

    elif "Remembering The Sacred Order" in quest_titles and has_fliers:
        state.scroll_typewriter("You are back in the familiar bustle of the Town Center.")
        while True:
            hand_out_fliers = input("\n\n\nDo you wish to hand out Earl's Fliers? (y/n): ").strip().lower()
            if hand_out_fliers == "y":
                state.scroll_typewriter("You begin handing out Earl's Fliers...")
                time.sleep(2)
                #earls_fliers_minigame_one() create a mini game here!
                success = True
                if success == True:
                    clear()
                    print("CONGRATULATIONS!!! You have successfully handed out all of Earl's Fliers.")
                    state.remove_from_inventory("Earl's Fliers")
                    print("\n\nINVENTORY UPDATED")
                    
                    
                break
            elif hand_out_fliers =="n":
                clear()
                break
            else:
                print("Invalid Selection. Please try again. ")
    else:
        state.scroll_typewriter("You are back in the familiar bustle of the Town Center.")
    
    

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    return prompt_player_action(state, allowed_directions={"north", "south", "east", "west", "apples"})

def bazaar(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Bazaar", {})
    clear()
    print(f"Location: Bazaar\n\n")

    if not location_state.get("visited", False):
        bazaar_text = "You step into the Bazaar for the first time."
        location_state["visited"] = True
    else:
        bazaar_text = "You are back in the familiar bustle of the Bazaar."

    state.scroll_typewriter(bazaar_text)
    input("\n\n\nPress enter to continue\n")

    # ----- Shop Interaction -----
    shop_items = state.get_shop_inventory()
    while True:
        clear()
        print("\n--- Shop Menu ---")
        print(f"Gold: {state.get_gold()}")
        for idx, (item, price) in enumerate(shop_items.items(), start=1):
            print(f"{idx}. {item} - {price} gold")
        print("0. Exit Shop")

        choice = input("Choose an item to buy (by number): ")

        if choice == "0":
            clear()
            print("You exit the shop.")
            time.sleep(2)
            break

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(shop_items):
                item_name = list(shop_items.keys())[index]
                item_price = shop_items[item_name]

                if state.get_gold() >= item_price:
                    state.set_gold(state.get_gold() - item_price)
                    inventory = state.get_inventory()
                    inventory.append(item_name)
                    state.set_inventory(inventory)
                    print(f"You bought {item_name}!")
                else:
                    print("You don't have enough gold.")
            else:
                print("Invalid selection.")
        else:
            print("Please enter a number.")
        
        time.sleep(2)

    # ----- Movement or Other Actions -----
    return prompt_player_action(state, allowed_directions={"east"})

def the_croftward(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Croftward", {})
    clear()
    print(f"Location: The Croftward\n\n")

    visited = location_state.get("visited", False)
    has_staff = "Wizard Staff" in state.get_inventory()


    if not visited and not has_staff:
        state.scroll_typewriter("You step into The Croftward for the first time. You don't have the staff yet to give to the wizard.")
        location_state["visited"] = True

    elif not visited and has_staff:
        state.scroll_typewriter("You step into The Croftward for the first time. You are finally able to return the staff to Elvis the Wizard.")
        location_state["visited"] = True
        state.complete_quest("Find the Bug Net")
        print("\n\nQUEST LOG UPDATED")
        input("Press ENTER to continue")

    elif visited and not has_staff:
        state.scroll_typewriter("You are back in the familiar street of The Croftward. You still don't have the staff to return to the wizard.")

    elif visited and has_staff:
        state.scroll_typewriter("You are back in the familiar street of The Croftward. You are finally able to return the staff to Elvis the Wizard.")
        state.complete_quest("Find the Bug Net")
        print("\n\nQUEST LOG UPDATED")
        input("Press ENTER to continue")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    return prompt_player_action(state, allowed_directions={"north"})

def eastern_orchard(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Eastern Orchard", {})

    clear()
    print(f"Location: Eastern Orchard\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    bennyboy_visited = location_state.get("bennyboy", False)
    has_bugnet = "Bug Net" in state.get_inventory()
    bugnet_quest_completed = state.is_quest_completed("Find the Bug Net")
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]

    # First time visiting
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("You step into the Eastern Orchard for the first time. You hear crying.")
    elif visited and not bennyboy_visited:
        state.scroll_typewriter("You step into the Eastern Orchard again. You hear the same distinct crying.")
    # Encounter logic
    if not bennyboy_visited:
        while True:
            print("\n\n1. Investigate the crying\n2. Retreat!")
            action = input("\nACTION: ").strip()

            if action == "1":
                if has_bugnet:
                    state.scroll_typewriter("""You investigate the crying and meet Benny Boy! He wants a bugnet. You give him one!
He gives you a jar containing 3 iridescent mango beetles.""")
                    location_state["bennyboy"] = True
                    state.remove_from_inventory("Bug Net")
                    state.add_to_inventory("3 Mango Beetles")

                    if "Find the Bug Net" not in quest_titles:
                        state.add_quest({
                            "title": "Find a Bug Net",
                            "description": "Benny Boy needs a bug net to catch his favorite bugs.",
                            "status": "Active"
                        })

                    state.complete_quest("Find the Bug Net")
                    print("\n\nQUEST LOG UPDATED")
                    
                else:
                    state.scroll_typewriter("You investigate the crying and meet Benny Boy! He wants a bugnet. You don't have one.")
                    location_state["bennyboy"] = True

                    if "Find the Bug Net" not in quest_titles:
                        state.add_quest({
                            "title": "Find the Bug Net",
                            "description": "Benny Boy needs a bug net to catch his favorite bugs.",
                            "status": "Active"
                        })
                    print("\n\nQUEST LOG UPDATED")
                    
                break

            elif action == "2":
                state.scroll_typewriter("You chicken out and go back. Shame on you.")
                return prompt_player_action(state, allowed_directions={"north", "west"})
            else:
                print("Invalid choice. Try again.")
                time.sleep(2)
                clear()

    # Already met Benny Boy
    elif bennyboy_visited:
        if has_bugnet and not bugnet_quest_completed:
            state.scroll_typewriter("""You step into the Eastern Orchard again. You see Benny Boy. He asks about the bug net. You give him one!
He gives you a jar containing 3 iridescent mango beetles.""")

            state.remove_from_inventory("Bug Net")
            state.add_to_inventory("3 Mango Beetles")
            state.complete_quest("Find the Bug Net")

        elif not has_bugnet and not bugnet_quest_completed:
            state.scroll_typewriter("You step into the Eastern Orchard again. You see Benny Boy. He asks about the bug net you don't have.")

        else:
            state.scroll_typewriter("Benny Boy is playing with his new beetles. He's no longer crying.")
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    return prompt_player_action(state, allowed_directions={"north", "west"})

def windshire_chapels(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Windshire Chapels", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_fliers = "Earl's Fliers" in state.get_inventory()
    clear()
    
    print(f"Location: Windshire Chapels\n\n")
    if not location_state.get("visited", False): #If you enter for the first time
        state.scroll_typewriter("You step into the Windshire Chapels for the first time. You meet Earl the Hallowed Knight. He give you fliers to pass around town.")
        location_state["visited"] = True  # Update visited flag
        # Handle Quest giving below
        if "Remembering The Sacred Order" not in quest_titles:
            state.add_quest({
                "title": "Remembering The Sacred Order",
                "description": "Earl needs you to hand out these fliers in the Town Center.",
                "status": "Active"
            })
            state.add_to_inventory("Earl's Fliers")
            print("\n\nQUEST LOG AND INVENTORY UPDATED")
            
    
    elif location_state.get("visited", True) and not has_fliers: # If you return having completed the quest
        state.scroll_typewriter("You report to Earl that you delivered the fliers. He in return gives you a Potion of Healing!")
        state.complete_quest("Remembering The Sacred Order")
        state.add_to_inventory("Potion of Healing")
        print("\n\nQUEST LOG AND INVENTORY UPDATED")
        
    else: # If you return but still have the fliers
       state.scroll_typewriter("You step into the Windshire Chapels once more. Earl is dissapointed you still haven't passed out his fliers.")
    
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    return prompt_player_action(state, allowed_directions={"south"})

def forest_entrance(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Forest Entrance", {})
    visited = location_state.get("visited", False)
    witch_defeated = location_state.get("bennyboy", False)
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_staff = "Wizard Staff" in state.get_inventory()
    clear()
    
    print(f"Location: Forest Entrance\n\n")
    if not visited: #If you enter for the first time
        state.scroll_typewriter("You reach the edge of the woods. You meet Tannenbark, the enchanted squirrel.")
        location_state["visited"] = True  # Update visited flag
        
    
    elif visited and not has_staff and not witch_defeated: # If enter but don't have the staff
        state.scroll_typewriter("You return to the edge of the woods. Tannenbark is wondering if you really know where you're going.")

    elif visited and has_staff and not witch_defeated: # If enter and do have the staff, encounter the Hag!!!
        state.scroll_typewriter("You return to the edge of the woods. You encounter the Witch! She wants the wizard staff back!")
        # witch_combat()       toggle witch combat when updated
        success = True
        if success:
            location_state["witch_defeated"] = True

    elif witch_defeated: # If you have already defeated the witch
        state.scroll_typewriter("You return to the edge of the woods. You remember how bravely you defeated the witch.")

    
    
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    return prompt_player_action(state, allowed_directions={"south","west"})

def abandoned_hut(state):
    pass

# GAME LOOP
def game_loop():

    state = GameState()
    run = True

    while run:
        clear()
        run_game_title_menu(state)
        clear()
        
        while run:
            location = state.get_location()

            if location == "prelude":
                prelude(state)
                state.set_location("town_center")  # Move the player after prelude
                continue  # Go back to the start of the inner loop

            elif location == "town_center":
                # Show the scene once
                action = town_center(state)  # town_center will now call prompt_player_action internally

                # Only handle map transitions here
                if action == "west":
                    print("You go West")
                    time.sleep(1)
                    state.set_location("bazaar")
                elif action == "south":
                    print("You go South")
                    time.sleep(1)
                    state.set_location("the_croftward")
                elif action == "north":
                    print("You go North")
                    time.sleep(1)
                    state.set_location("forest_entrance")
                elif action == "east":
                    print("You go East")
                    time.sleep(1)
                    state.set_location("eastern_orchard")
                elif action == "apples":
                    print("A secret hatch opens inside the fountain!")
                    time.sleep(1)
                    pass # ADD SECRET HERE!
            
            elif location == "bazaar":
                action = bazaar(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("town_center")

            elif location == "the_croftward":
                action = the_croftward(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("town_center")

            elif location == "eastern_orchard":
                action = eastern_orchard(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("windshire_chapels")
                    elif action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("town_center")
            
            elif location == "windshire_chapels":
                action = windshire_chapels(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("eastern_orchard")

            elif location == "forest_entrance":
                action = forest_entrance(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("abandoned_hut")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("town_center")
            
            elif location == "abandoned_hut":
                action = abandoned_hut(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("forest_entrance")
                    
            else:
                print(f"Unknown location: {location}")
                run = False



# Run the game please
game_loop()