import json
import os
import re
import time


# SET CONSTANTS
SPEED = 0.01 # The smaller the faster
FOLDER_PATH = "C:/Users/Aaron/OneDrive/Documents/GitHub/whittershok/game_saves"
os.makedirs(FOLDER_PATH, exist_ok=True)


# Special Semantics for Terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear') #Clears on both Windows and Mac


class GameState:
    def __init__(self):
        self.name = ""
        self.gold = 0
        self.quest_log = []
        self.inventory = []
        self.location = ""
        self.shop_inventory = {}
        self.world_state = {}

    def create_new(self):
        self.name = input("Enter character name: ")
        self.gold = 0
        self.quest_log = []
        self.inventory = ["Spoon"]
        self.location = "prelude"
        self.shop_inventory = {"Bug Net": 5, "Shovel": 25, "Apple Pie": 10, "Broken Dagger": 7, "Sharpening Stone": 20}
        self.world_state = {
        
        # City Areas
        "Town Center": {
            "visited": False,
        },
        "Bazaar": {
            "visited": False,
        },
        "The Croftward": {
            "visited": False,
        },
        
        "The Gallows": {
            "visited": False,
        },
        "Northern Streets": {
            "visited": False
        },
        "City Hall": {
            "visited": False,
            "failed_visited": False,
            "success_visited": False,
        },
        "The Graveyard": {
            "visited": False,
            "sad_woman": False,
        },
        "Wizard Tower": {
            "visited": False,
            "staff": False,
            "tablet": False,
        },
        "The Barracks": {
            "visited": False,
            "signet": False,
        },
        "The Keep Entrance": {
            "visited": False,
            "invited": False,
        },
        "North Gate": {
            "visited": False,
        },
        "East Gate": {
            "visited": False,
        },
        "South West Gate": {
            "visited": False,
        },

        # Eastern Areas
        "Eastern Orchard": {
            "visited": False,
            "bennyboy": False,
        },
        "Abandoned Lumber Camp": {
            "visited": False,
            "wood_taken": False,
            "clear_path": False,
        },
        "Angel Crossing": {
            "visited": False,
            "bridge_built": False,
        },

        # Southern Areas
        "Windshire Chapels": {
            "visited": False,
            "fliers": False
        },
        "Southern Outskirts": {
            "visited": False,
        },


        # Forest Areas
        "Forest Entrance": {
            "visited": False,
            "witch_defeated": False
        },
        "The Abandoned Hut":{
            "visited": False,
        },
        "Twilight Grove":{
            "visited": False,
            "fountain": False
        },
        "Dire Wolf Pines":{
            "visited": False,
        },  
        "Hunter's Cabin": {
            "visited": False,
        },
        "Cave Entrance": {
            "visited": False,
        },
        "The Tunnels": {
            "visited": False,
            "monster_defeated": False,
        },
        "The Barren Ridge": {
            "visited": False,
        },
        "Hollowpine Outpost": {
            "visited": False,
        }
        }
        
        

    def save_to_slot(self, slot):
        file_path = self._get_file_path(slot)

        data = {
            "name": self.name,
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


    # Dictionary to pull and update variables within CLASS
    # Getter for name
    def get_name(self):
        return self.name
    

    # Getter for gold
    def get_gold(self):
        return self.gold
    
    # Setter for gold
    def set_gold(self, new_amount):
        self.gold = new_amount

    # Adder for gold

    def add_gold(self, amount):
        self.gold = self.gold + amount


    
    # Getter for shop inventory
    def get_shop_inventory(self):
        return self.shop_inventory
    
    # Setter for shop inventory
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
    
    def is_quest_failed(self, title):
        for quest in self.quest_log:
            if quest["title"] == title:
                return quest["status"].lower() == "failed"
        return False
    
    # Complete quest
    def complete_quest(self, title):
        for quest in self.quest_log:
            if quest["title"] == title:
                quest["status"] = "Completed"

    def fail_quest(self, title):
        for quest in self.quest_log:
            if quest["title"] == title:
                quest["status"] = "Failed"
    # Adder to quest_log
    def add_quest(self, quest_dict):
        self.quest_log.append(quest_dict)


    # Getter for world_state
    def get_world_state(self):
        return self.world_state

    # Setter for world_state
    def set_world_state(self, new_world_state):
        self.world_state = new_world_state



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
    print(".-.-.-.-.-.-.-.-.-.-.-..-.-.")
    print("Game Menu")
    print("1. Create New Game")
    print("2. Load Game")
    print("3. Exit")
    choice = input("Select an option: ")

    if choice == "1":
        state.create_new()
        time.sleep(1)
        clear()
        return True
    elif choice == "2":
        slot = int(input("Enter save slot (1-3): "))
        state.load_from_slot(slot)
        return True
    elif choice == "3":
        return False
    else:
        print("Invalid choice. Try again.")

def show_inventory(state):
    clear()
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
            print()
            

    input("Press Enter to return...")


def prompt_player_action(state, allowed_directions=None):
    if allowed_directions is None:
        allowed_directions = {}

    while True:
        # time.sleep(1)
        clear()
        location = state.get_location()
        formatted_location = location.replace("_", " ").title()
        print(f"Location: {formatted_location}\n\n")

        print("Available directions:")
        if allowed_directions:
            
            for dir_key, dest in allowed_directions.items():
                dest_name = dest.replace("_", " ").title()
                print(f" - {dest_name} ({dir_key.title()})")

            print()
        else:
            print(" - None available")
        
        print(f"Gold: {state.get_gold()}     (I) Inventory   (Q) Quest Log   (S) Save Game   (E) Exit Game")
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
            time.sleep(1)
            clear()
        

        elif action == "e":
            confirm = input("Are you sure you want to quit? (y/n): ").strip().lower()
            if confirm == "y":
                action = "quit"
                return action
                
            else:
                clear()

        else:
            print("You can't go that way. Try again.")
            time.sleep(1)
            clear()


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
It’s strange. Wizards are usually too busy muttering at scrolls or accidentally exploding sheep to ask favors of others—especially 
from someone as aggressively average as you.

You’re not strong. You’re not clever. People don’t dislike you—they just don’t often remember you exist.

But never mind all that. Your backstory is short, your socks don’t match, and destiny apparently doesn’t care.

[pause]"""
    
    state.scroll_typewriter(intro_text)
    
    input("\n\nPress ENTER to continue")
       
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
            "description": "Elvis the wizard needs his Staff, stolen by the Old Hag. Something strange is happening.",
            "status": "Active"
        })
    
    clear()
    
    print(f"Location: Town Center\n\n")
    if not location_state.get("visited", False):
        print()
        slot = int(input("Enter save slot (1-3): "))
        state.save_to_slot(slot)
        time.sleep(1)
        clear()
        print(f"Location: Town Center\n\n")
        state.scroll_typewriter("""You step into the Town Center for the first time. The wizard is there waiting for you. 
"[name]! My dear friend! Oh it's great to see young people like you getting around. Thanks for arriving in a timely manner. 
I am in dire need of my staff! My right knee is throbbing, telling me that something mysterious is going on around here and
just last night my staff went missing! You know, my magical staff has drawn the attention of many a creature. But I know it was that old hag 
Griselda. Always jealous of my magical instruments. She's a formidable magic-user, but her greatest weakness, if you can 
believe it, is her overwhelming vanity. Oh, she prides herself on her beauty." Elvis shakes his head, and you note that this old hag
is anything but beauty. 
                                
"One time we were in a duel and she nearly dissolved when she caught a glimpse of her own reflection in a still pond! The old fool is terribly 
sensitive about her looks."

"Her hut is somewhere in the woods, but I recommend getting yourself well equipped before venturing out there. It's full of
dangerous spirits and fearsome wolves. Here, go find yourself something useful in the Bazaar." He hands you 5 gold with a wink.

"I'll be in my wizard tower for when you return with the staff."
He shakes your hand and begins walking southward. He shouts "May magic by thy guide!" """)
        state.add_gold(5)
        print("\n\n\nQUEST LOG AND INVENTORY UPDATED")
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
    
    available_directions = {
        "north": "The Gallows",
        "east": "East Gate",
        "south": "The Croftward",
        "west": "The Bazaar"
    }
    action = prompt_player_action(state, available_directions)
    return action
    
def bazaar(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Bazaar", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_wolf_skins = "Wolf Skins" in state.get_inventory()

    clear()
    print(f"Location: Bazaar\n\n")

    if not location_state.get("visited", False):
        state.scroll_typewriter("""
You step into the Bazaar, a bustling place of chaos. Stalls overflow with exotic goods, merchants hawk their wares 
in booming voices, and the air is thick with the scent of spices and foreign incense. 

Amidst the lively chaos, a man with a wild, untamed beard and keen, intelligent eyes emerges from behind a counter piled high with cured pelts 
and leather goods. He's Wyatt Coonsmith, and a genuine, if slightly weathered, smile spreads across his face as he extends a calloused hand. 

"Well now, don't often see a fresh face like yours around here," he rumbles, his voice carrying a warmth that cuts through the market's din. 
He sighs, glancing north. "Truth be told, I'm facing quite a predicament. Winter's coming on, and I'm in desperate need of dire wolf pelts 
from the Northern Forest for my sales, but the forest... it's a dangerous place these days. That phantom's got the guards at the North Gate on 
high alert, only letting folk of 'higher standing' through. A true shame, with such fine pelts just waiting." """)
        
        print("\n\nQUEST LOG UPDATED")
        if "Howl You Help Me" not in quest_titles:
            state.add_quest({
                "title": "Howl You Help Me",
                "description": "Wyatt needs fresh wolf pelts fast for the upcoming winter sales.",
                "status": "Active"
            })
        if has_wolf_skins:
            state.complete_quest("Howl You Help Me")
            state.scroll_typewriter("You hand over the wolf skins and he is in so much awe at how beautiful they are. In return, he rewards you with 40 gold pieces.")
            state.add_gold(40)
            print("QUEST LOG AND INVENTORY UPDATED")
        location_state["visited"] = True
    else:
        state.scroll_typewriter("You are back in the familiar bustle of the Bazaar. You approach Wyatt's store.")
        if has_wolf_skins:
            state.complete_quest("Howl You Help Me")
            state.scroll_typewriter("You hand over the wolf skins and he is in so much awe at how beautiful they are. In return, he rewards you with 40 gold pieces.")
            state.add_gold(40)
            print("QUEST LOG AND INVENTORY UPDATED")

    input("\n\nPress enter to continue\n")

    # ----- Shop Interaction -----
    shop_items = state.get_shop_inventory()
    while True:
        clear()
        print("\n--- Shop Menu ---")
        print(f"Gold: {state.get_gold()}")
        for idx, (item, price) in enumerate(shop_items.items(), start=1):
            print(f"{idx}. {item} - {price} gold")
        print("\nE) Exit Shop")

        choice = input("Choose an item to buy (by number): ").strip().lower()

        if choice == "e":
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
                    if item_name in state.shop_inventory: # Removes item from shop inventory
                        del state.shop_inventory[item_name] 
                    state.add_to_inventory(item_name) # Update player inventory
                    print(f"You bought {item_name}!")
                else:
                    print("You don't have enough gold.")
            else:
                print("Invalid selection.")
        else:
            print("Please enter a number.")
        
        time.sleep(2)

    # ----- Movement or Other Actions -----
    available_directions = {
        "north": "Northern Streets",
        "east": "Town Center",
        "south": "The Graveyard",
        "west": "The Barracks",
    }
    return prompt_player_action(state, available_directions) 

def wizard_tower(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Wizard Tower", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    clear()
    print(f"Location: Wizard Tower\n\n")

    visited = location_state.get("visited", False)
    has_staff = "Wizard Staff" in state.get_inventory()


    if not visited and not has_staff:
        state.scroll_typewriter("You approach the Wizard Tower for the first time. You don't have the staff yet to give to the wizard.")
        location_state["visited"] = True

    elif not visited and has_staff:
        state.scroll_typewriter("You enter the Wizard Tower for the first time. You are finally able to return the staff to Elvis the Wizard.")
        location_state["visited"] = True
        state.complete_quest("Return The Wizard Staff")
        print("\n\nQUEST LOG UPDATED")
        

    elif visited and not has_staff:
        state.scroll_typewriter("You are back at Elvis's tower. You still don't have the staff to return to him yet.")

    elif visited and has_staff:
        state.scroll_typewriter("You return to the Wizard Tower and enter. You are finally able to return the staff to Elvis the Wizard.")
        state.complete_quest("Return The Wizard Staff")
        print("\n\nQUEST LOG AND INVENTORY UPDATED")
        input("\n\n\nPress enter to continue\n")
        state.scroll_typewriter("""
He shakes your hand eagerly with gratitude and excitement and then begins caressing his long-lost wizard staff.
You begin to leave when he stops you and gives you a pouch of 15 gold! He then tells you, 'I have another favor, dear friend.
'Deep within the southern pyramids, there is an ancient relic known as the Burning Tablet. This is meant to be used to seal
portals that open from other realms to protect our plain of existence from becoming corrupted. We are in dire need of this
realm protector as there is a portal opening this very instance!'

[pause]
The wizard points out his high-tower window and you see a giant purple pillar descending to the Earth off towards the West. 
'It is up to you, [player_name] to save humanity.' Depart with haste!""")
        
        if "Retrieve the Burning Tablet" not in quest_titles:
            state.add_quest({
                "title": "Retrieve the Burning Tablet",
                "description": "The fate of humanity is in your hands! Find the Burning Tablet in the Southern Desert and Return it to Elvis.",
                "status": "Active"
            })
        print("\n\nQUEST LOG UPDATED")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    
    available_directions = {
        "west": "The Croftward",
    }
    return prompt_player_action(state, available_directions)

def the_croftward(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Croftward", {})

    clear()
    print(f"Location: The Croftward\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("You enter the Croftward for the first time. This place is known as the poorer side of the housing district of the city.")
    else:
        state.scroll_typewriter("You return to the Croftward, a few people are muttering to each other as you walk through.")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "Town Center",
        "east": "Wizard Tower",
        "west": "The Graveyard",
    }
    return prompt_player_action(state, available_directions)

def northern_streets(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Northern Streets", {})

    clear()
    print(f"Location: Northern Streets\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("You pass through the northern streets for the first time.")
    else:
        state.scroll_typewriter("You return to the northern streets.")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "North Gate",
        "east": "The Gallows",
        "south": "The Bazaar",
        "west": "City Hall",
    }
    return prompt_player_action(state, available_directions)

def the_gallows(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Gallows", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_letter = "Executioner's Letter" in state.get_inventory()
    clear()
    print(f"Location: The Gallows\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited and not has_letter:
        location_state["visited"] = True
        state.scroll_typewriter("""
A grim silence hangs over the gallows, a stark contrast to the distant bustle of the Town Center. The wooden platform stands starkly against 
the sky, ropes dangling ominously, swaying ever so slightly in the breeze. A lone, burly executioner stands nearby, sharpening his axe with 
slow, deliberate strokes, his back to you. The air feels heavy with anticipation, but nothing is happening right now, just the quiet, 
unsettling wait.""")
    elif visited and not has_letter:
        state.scroll_typewriter("""
The gallows stand as grim and silent as before, the vacant platform waiting under a still sky. The burly executioner is still present, 
methodically polishing his axe. He pays you no mind, his focus solely on his chilling task, and the heavy atmosphere here has not changed.""")
    
    elif "A Favor for Flavor" in quest_titles and has_letter:
        state.scroll_typewriter("""
A tense hush has fallen over the gallows. A small, somber crowd has gathered, their faces etched with grim expectation. On the platform, a 
hooded figure stands before the noose, while the burly executioner finishes his final preparations, his movements deliberate and unhurried. 
A city guard stands by, ready to give the signal. The air crackles with an unsettling stillness, broken only by the distant calls of gulls 
and the faint murmur of prayers. 
                                
This is your chance.""")
        
        while True:
            hand_out_fliers = input("\n\n\nDo you wish to deliver the Executioner's Letter? (y/n): ").strip().lower()
            print("\n\n")
            if hand_out_fliers == "y":
                clear()
                state.scroll_typewriter("""
You quickly step forward, pushing through the hushed crowd towards the platform. The executioner, his hand already on the lever, turns as 
you approach, his expression unreadable beneath his grim hood. 
                                        
"Wait!" you call out, extending Henry's crumpled letter towards him. He takes it, his eyes scanning the contents, and then, with a heavy sigh, 
lowers his hand from the lever. The tension in the air immediately dissipates as the guard beside him looks on, confused. The hooded figure 
on the platform sags in relief.""")
                print("\n\n")
                print("CONGRATULATIONS!!! You have successfully stopped the execution!")
                state.remove_from_inventory("Executioner's Letter")
                state.complete_quest("A Favor for Flavor")
                print("\nINVENTORY UPDATED")
                    
                break

            elif hand_out_fliers =="n":
                clear()
                state.scroll_typewriter("""
You hesitate, the letter clutched in your hand as the silence at the gallows stretches. The guard gives the signal, and with a creak of wood, 
the executioner pulls the lever. A gasp ripples through the crowd, and a moment later, only the rhythmic sway of the rope remains. 
The grim task is done.""")
                print()
                print("YOU FAILED. You did not stop the execution.")
                state.fail_quest("A Favor for Flavor")
                print("\n\nQUEST LOG UPDATED")  

                break

            else:
                print("Invalid Selection. Please try again. ")
    else:
        state.scroll_typewriter("""
A grim silence has settled over the gallows, but today it feels different. The platform stands stark against the sky, ropes still swaying, 
but the tension that once hung heavy in the air is gone, replaced by an unsettling stillness. The executioner is nowhere to be seen, and 
the small crowd has dispersed, leaving the stark wooden structure alone with its grim history.""")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "south": "Town Center",
        "west": "Northern Streets",
    }
    return prompt_player_action(state, available_directions)

def the_barracks(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Barracks", {})
    shovel_trouble_active = state.is_quest_active("Shovel Trouble")
    has_shovel = "Shovel" in state.get_inventory()
    clear()
    print(f"Location: The Barracks\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not has_shovel:

        if not visited and not shovel_trouble_active:
            location_state["visited"] = True
            state.scroll_typewriter("""
You step into the Barracks, the air thick with the scent of oiled leather and steel. Dominating one wall is an impressive display, 
not just of shining swords and gleaming axes, but also an odd assortment of well-maintained shovels, pickaxes, and other sturdy 
gardening tools hanging alongside them.""")
        elif not visited and shovel_trouble_active:
            location_state["visited"] = True
            state.scroll_typewriter("""
You step into the Barracks, the air thick with the scent of oiled leather and steel. Dominating one wall is an impressive display, 
not just of shining swords and gleaming axes, but also an odd assortment of well-maintained shovels, pickaxes, and other sturdy 
gardening tools hanging alongside them.""")
            while True:
                answer = input("\n\nDo you take a shovel? (y/n): ").strip().lower()
                if answer == "y":
                    print("\n\nINVENTORY UPDATED")
                    state.add_to_inventory("Shovel")
                    time.sleep(2)
                    break
                elif answer == "n":
                    print("You decide it would be best not to take one.")
                    time.sleep(2)
                    break
                else:
                    print("\nInvalid input. Please try again.")

        elif visited and not shovel_trouble_active:
            state.scroll_typewriter("""
You return to the Barracks, the familiar scent of steel and leather welcoming you back. The impressive wall display of both weapons and 
gardening tools stands just as you left it.""")
            
        elif visited and shovel_trouble_active:
            state.scroll_typewriter("""
You return to the Barracks, the familiar scent of steel and leather welcoming you back. The impressive wall display of both weapons and 
gardening tools stands just as you left it.""")
            while True:
                answer = input("\n\nDo you take a shovel? (y/n): ").strip().lower()
                if answer == "y":
                    print("\n\nINVENTORY UPDATED")
                    state.add_to_inventory("Shovel")
                    time.sleep(2)
                    break
                elif answer == "n":
                    print("You decide it would be best not to take one.")
                    time.sleep(2)
                    break
                else:
                    print("\nInvalid input. Please try again.")
    elif has_shovel:
        state.scroll_typewriter("""
You return to the Barracks, the familiar scent of steel and leather welcoming you back. Some gaurds are looking at the spot where the 
shovel used to rest.""")
        
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "east": "The Bazaar",
        "south": "South West Gate",
        "west": "The Keep Entrance",
    }
    return prompt_player_action(state, available_directions)

def city_hall(state):
    world_state = state.get_world_state()
    location_state = world_state.get("City Hall", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_letter = "Executioner's Letter" in state.get_inventory()
    favor_for_flavor_completed = state.is_quest_completed("A Favor for Flavor")
    favor_for_flavor_failed = state.is_quest_failed("A Favor for Flavor")
    clear()
    print(f"Location: City Hall\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    failed_visited = location_state.get("failed_visited", False)
    success_visited = location_state.get("success_visited", False)
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("""
The grand doors of City Hall swing open, revealing a bustling scene of bureaucratic chaos. The air crackles with the low murmur of heated arguments 
and the scratch of quills on parchment. Citizens gesticulate wildly, guards attempt to maintain order, and the sharp scent of stale ink hangs heavy. 
Amidst the clamor, a young man with a furrowed brow, wearing the distinct livery of a squire, spots you. 

"Gods above, child, you look like you haven't had a proper meal in weeks!" he exclaims, rushing over with an agitated shuffle. 
"I'm Henry, and I'm in a bind. I've accidentally approved an execution at the gallows, and my duties here chain me. Deliver this letter to the 
executioner immediately—it's a reprieve! Do this, and I'll ensure your name is on Lord Circumbus's feast invitation. 
A good meal is the least you deserve!" """)
        
        if "A Favor for Flavor" not in quest_titles:
            state.add_quest({
                "title": "A Favor for Flavor",
                "description": "Henry the Squire is in a bind. Deliver the letter to the executioner at the gallows immediately!",
                "status": "Active"
            })
            state.add_to_inventory("Executioner's Letter")
        print("\n\nQUEST LOG AND INVENTORY UPDATED")
        # Add potential quest here to get invited to the king's feast
    elif not failed_visited and not success_visited:
        if visited and favor_for_flavor_completed:
            state.scroll_typewriter("""
You find Henry the Squire still amidst the chaos of City Hall, though he looks considerably less stressed. His eyes light up as he sees you. 
"Ah, there you are! I saw the gallows; your timing was impeccable! You've saved me a lifetime of guilt, truly. As promised, your name is 
now on the guest list for Lord Circumbus's feast. Enjoy a proper meal for once—you've certainly earned it!" """)
            location_state["success_visited"] = True
            print("\n\nQUEST LOG UPDATED")

        elif visited and has_letter:
            state.scroll_typewriter("""
The City Hall remains a whirlwind of activity, with clerks shouting, citizens clamoring, and the low hum of endless disputes filling the 
air. You spot Henry the Squire, still looking harried, deep in conversation with a stern-faced guard. He glances your way, offers a quick, 
distracted nod, and then turns back to his urgent paperwork, clearly too busy to offer another word.""")
            
        elif favor_for_flavor_failed:
            state.scroll_typewriter("""
You find Henry the Squire still amidst the chaos of City Hall, but before you can approach, two stern city guards seize him by the arms. 
"Henry Albright, you're under arrest for dereliction of duty and obstruction of justice!" one barks. 
                                
Henry's eyes, wide with panic, lock onto yours across the bustling hall. "You! This is your fault!" he shouts, struggling against the guards 
as they drag him away, his accusation echoing briefly through the clamor.""")
            location_state["failed_visited"] = True
    elif success_visited:
        state.scroll_typewriter("""
The grand doors of City Hall swing open, and you step into the familiar cacophony of shouting citizens and rustling papers. Henry the Squire 
is still at his desk, but today, a faint smile plays on his lips as he efficiently sorts through a stack of documents. He catches your eye, 
gives a polite nod of recognition, and then returns to his work, the crisis at the gallows long resolved thanks to your intervention. """)

    elif failed_visited:
        state.scroll_typewriter("""
You step into City Hall, and the usual clamor feels subdued, a strange quiet filling the spaces where Henry's frantic energy once was. His 
desk is now eerily tidy, cleared of the overflowing stacks of parchment and frantic notes, a stark testament to his sudden absence. The 
city guards and clerks go about their business with an air of practiced indifference, but the scene is a stark reminder of the swift 
consequences of your choices at the gallows.""")
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "east": "Northern Streets",
    }
    return prompt_player_action(state, available_directions)

def north_gate(state):
    world_state = state.get_world_state()
    location_state = world_state.get("North Gate", {})
    has_signet = "Royal Signet" in state.get_inventory()

    clear()
    print(f"Location: North Gate\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited and not has_signet:
        location_state["visited"] = True
        state.scroll_typewriter("""You approach the North gate for the first time. There are some soldiers gaurding the way. 
"Hold there, child. The path north is dangerous, teeming with wolves and shadows. Only those of true loyalty, bearing a mark 
of the crown, may pass freely." """)
        # ----- Movement or Other Actions -----
        input("\n\n\nPress enter to continue\n")
        available_directions = {
            "south": "Northern Streets"
        }
        return prompt_player_action(state, available_directions)
    
    elif visited and not has_signet:
        state.scroll_typewriter("""You return to the North gate and approach the soldiers. They still are content on not letting you pass through. 
You need some kind of item to appear as royalty.""")
        # ----- Movement or Other Actions -----
        input("\n\n\nPress enter to continue\n")
        available_directions = {
            "north": "Forest Entrance",
            "south": "Northern Streets",
        }
        return prompt_player_action(state, available_directions)
    
    elif not visited and has_signet:
        location_state["visited"] = True
        state.scroll_typewriter("""You approach the North gate for the first time. There are some soldiers gaurding the way. 
"Hold there, child. The path north is dangerous, teeming with wolves and shadows. Only those of true loyalty, bearing a mark 
of the crown, may pass freely." You show forth your signet and the guards part ways. You walk through the North gate.""")
    
    elif visited and has_signet:
        state.scroll_typewriter("""You return to the North gate and approach the soldiers. You show forth your signet and the guards part ways.""")
        
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "Forest Entrance",
        "south": "Northern Streets",
    }
    return prompt_player_action(state, available_directions)

def the_keep_entrance(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Keep Entrance", {})
    favor_for_flavor_completed = state.is_quest_completed("A Favor for Flavor") # Update Quest later
    clear()
    print(f"Location: The Keep Entrance\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited and not favor_for_flavor_completed:
        location_state["visited"] = True
        state.scroll_typewriter("You approach the magestic keep for the first time. You aren't on the invite list to the feast so you aren't allowed in.")
    elif not visited and favor_for_flavor_completed:
        location_state["visited"] = True
        state.scroll_typewriter("You approach the magestic keep for the first time. You are on the invite list. You may enter the Keep.")
    elif visited and not favor_for_flavor_completed:
        state.scroll_typewriter("You return to the magestic keep. You still aren't on the invite list to the feast so you aren't allowed in.")
    elif visited and favor_for_flavor_completed:
        state.scroll_typewriter("You return to the magestic keep. You are on the invite list. You may enter the Keep.")
      
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "east": "The Barracks",
        "west": "(Keep) Banquet Hall",
    }
    return prompt_player_action(state, available_directions)

def south_west_gate(state):
    world_state = state.get_world_state()
    location_state = world_state.get("South West Gate", {})

    clear()
    print(f"Location: South West Gate\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("You approach the South West gate for the first time.")
    else:
        state.scroll_typewriter("You return to the South West gate.")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "The Barracks",
        "south": "Southern Outskirts",
        "west": "Windshire Chappels"
    }
    return prompt_player_action(state, available_directions)

def the_graveyard(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Graveyard", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    shovel_trouble_completed = state.is_quest_completed("Shovel Trouble")
    the_grave_robbers_stash_completed = state.is_quest_completed("The Grave Robber's Stash")
    has_shovel = "Shovel" in state.get_inventory()
    clear()
    print(f"Location: The Graveyard\n\n")

    # Set Flags
    visited = location_state.get("visited", False)  
    sad_woman = location_state.get("sad_woman", False)  
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("""
A somber silence hangs over the Graveyard. Weathered tombstones lean at odd angles, some half-swallowed by tangled vines and overgrown grass. 
In the midst of this mournful tranquility, an old man is hunched over a freshly dug patch of dirt, muttering to himself. He 
clutches a broken shovel, its snapped handle resting uselessly in his hand, and his eyes dart nervously around, as if expecting someone.
His narrow eyes meet yours as you approach.
"Hey! You there! A young, capable sort, by the looks of it. Listen, I'm... uh... overseeing some important burials here, very sensitive work. 
And wouldn't you know it, I've had a terrible mishap! Buried ol' Silas in young Martha's plot! My last shovel just bit the dust." 
He gestures to the broken tool. "Fetch me a new shovel, quickly now, and I'll make it worth your while. A handsome share of... Silas's effects!" """)
        if "Shovel Trouble" not in quest_titles:
            state.add_quest({
                "title": "Shovel Trouble",
                "description": "An old man needs a new shovel to dig up a misplaced body.",
                "status": "Active"
            })
    elif not shovel_trouble_completed:
        if visited and not has_shovel:
            state.scroll_typewriter("""
The graveyard remains steeped in its melancholic silence, the leaning gravestones and overgrown paths unchanged. The old man is still hunched 
over the same patch of disturbed earth, his broken shovel a pathetic sight beside him. He glances up as you approach, his eyes still darting 
nervously, and without preamble, he gestures impatiently towards his useless tool. 

"Still here, eh? Did you bring it? The shovel, I mean! Ol' Silas isn't getting any fresher down there, and Martha certainly isn't getting 
any happier!" """)
        
        elif visited and has_shovel:
            state.scroll_typewriter("""
As you approach, the old man's eyes light up, fixing on the shovel in your hand. "Ah, there it is! A beauty!" he cackles, snatching it from you 
with surprising speed. He thrusts the shovel into the loose earth, digging with frantic energy. Within moments, the thud of wood on bone echoes, 
and he grunts with satisfaction, pulling something small and glinting from the unearthed grave. 

"Aha! Right then, a deal's a deal!" He shoves 25 gold pieces into your palm. "Thanks for the discretion! You're a true lifesaver. Now, if 
you'll excuse me, pressing engagements!" With a final, shifty glance, he scurries off, disappearing quickly from the graveyard, 
leaving you alone with the freshly disturbed grave and the shovel still sticking out of the dirt.""")
            state.complete_quest("Shovel Trouble")
            state.add_gold(25)
            state.remove_from_inventory("Shovel")
            print("\n\nQUEST LOG AND INVENTORY UPDATED")

    elif shovel_trouble_completed and not the_grave_robbers_stash_completed:
        if not sad_woman:
            state.scroll_typewriter("""
The graveyard is no longer empty. Two city guards stand near the freshly disturbed patch of earth, their expressions stern as they speak in 
hushed tones. A sobbing woman, clearly distraught, kneels by a nearby tombstone, her shoulders shaking. As you approach, you can overhear their 
conversation. 
                                
"I tell you, Officer, it was him again!" the woman wails, wiping tears from her eyes. "That wretched old grave robber, always after some 
ill-gotten gain! First he desecrates Silas's grave, now he's vanished! Everyone knows he's nothing but a notorious burglar, always hiding his 
dirty loot in some stash in the northern forest. It would be a miracle if someone could ever find it and bring him to justice!" The guards nod 
grimly, surveying the disturbed grave. The old man is long gone, leaving behind only the messy mound of dirt and a palpable sense of injustice 
hanging in the cool air.
""")
            location_state["sad_woman"] = True
            if "The Grave Robber's Stash" not in quest_titles:
                state.add_quest({
                    "title": "The Grave Robber's Stash",
                    "description": "The old man who staged as a graveyard caretaker has a hidden stash somewhere in the forest.",
                    "status": "Active"
                })
            print("\n\nQUEST LOG UPDATED")
        
        elif sad_woman:
            state.scroll_typewriter("""
The graveyard's quiet returns, the somber atmosphere once again dominated by the leaning gravestones and whispering breeze. The city guards 
are gone, leaving only the crying woman, still kneeling by Silas's disturbed grave. Her shoulders shake with silent sobs, and as you draw 
near, you can hear her soft, heartbroken muttering. "That old grave robber... he'll pay... he'll pay..." she whispers, her voice barely audible 
above the rustling leaves, hinting at a deep desire for justice and a hidden retribution for the desecration.""")

    elif the_grave_robbers_stash_completed:
        pass
        #Add Logic here

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "The Bazaar",
        "east": "The Croftward",
    }
    return prompt_player_action(state, available_directions)

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
                            "title": "Find the Bug Net",
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
                # ----- Movement or Other Actions -----
                input("\n\n\nPress enter to continue\n")
                available_directions = {
                    "north": "Abandoned Lumber Camp",
                    "east": "Angel Crossing",
                    "west": "East Gate",
                }
                return prompt_player_action(state, available_directions)
            else:
                print("Invalid choice. Try again.")
                time.sleep(2)
                clear()

    # Already met Benny Boy
    elif bennyboy_visited:
        if has_bugnet and not bugnet_quest_completed:
            state.scroll_typewriter("""You step into the Eastern Orchard again. You see Benny Boy. He asks about the bug net. You give him one!
He gives you a jar containing iridescent mango beetles.""")

            state.remove_from_inventory("Bug Net")
            state.add_to_inventory("Mango Beetles")
            state.complete_quest("Find the Bug Net")

        elif not has_bugnet and not bugnet_quest_completed:
            state.scroll_typewriter("You step into the Eastern Orchard again. You see Benny Boy. He asks about the bug net you don't have.")

        elif bugnet_quest_completed:
            state.scroll_typewriter("Benny Boy is playing with his new beetles. He's no longer crying.")
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "Abandoned Lumber Camp",
        "east": "Angel Crossing",
        "west": "East Gate",
    }
    return prompt_player_action(state, available_directions)

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
        state.scroll_typewriter("You report to Earl that you delivered the fliers. He in return gives you a Holy Stone of Banishing!")
        state.complete_quest("Remembering The Sacred Order")
        state.add_to_inventory("Holy Stone of Banishing")
        print("\n\nQUEST LOG AND INVENTORY UPDATED")
        input("Press ENTER to continue")
        
        
        
    else: # If you return but still have the fliers
       state.scroll_typewriter("You step into the Windshire Chapels once more. Earl is dissapointed you still haven't passed out his fliers.")
    
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "east": "South West Gate",
    }
    return prompt_player_action(state, available_directions)

def east_gate(state):

    world_state = state.get_world_state()
    location_state = world_state.get("East Gate", {})

    clear()
    print(f"Location: East Gate\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("You approach the East gate for the first time.")
    else:
        state.scroll_typewriter("You return to the East gate.")

    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "east": "Eastern Orchard",
        "west": "Town Center",
    }
    return prompt_player_action(state, available_directions)

def abandoned_lumber_camp(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Abandoned Lumber Camp", {})
    visited = location_state.get("visited", False)
    clear()
    print(f"Location: Abandoned Lumber Camp\n\n")
    has_interacted = False
    while not location_state.get("clear_path", False): # Directly check location_state for clarity
        # Update flags at the beginning of each main loop iteration
        has_rusty_saw = "Rusty Saw" in state.get_inventory()
        has_shiny_saw = "Shiny Saw" in state.get_inventory()
        has_sharpening_stone = "Sharpening Stone" in state.get_inventory()
        
    

        
        # --- Handle acquiring/using tools to clear the path ---
        if not has_rusty_saw and not has_shiny_saw:
            if has_interacted == False:
                state.scroll_typewriter("""You approach the Abandoned Lumber Camp, but the path is obstructed by a fallen log.""")
                has_interacted = True

            
            while True:
                state.scroll_typewriter("""Nearby you see an assortment of rusty tools.""")
            
                player_choice = input("\n\nDo you wish to pick up the Rusty Saw? (y/n): ").strip().lower()
                if player_choice == "y":
                    print()
                    state.scroll_typewriter("You pick up the Rusty Saw.")
                    state.add_to_inventory("Rusty Saw")
                    has_rusty_saw = "Rusty Saw" in state.get_inventory() #update inside 
                    print("\n\nINVENTORY UPDATED")
                    break
                elif player_choice == "n":
                    state.scroll_typewriter("\nYou decide not to pick up the Rusty Saw. The path remains obstructed.")
                            # ----- Movement or Other Actions -----
                    input("\n\n\nPress enter to continue\n")
                    available_directions = {
                        "south": "Eastern Orchard",
                    }
                    return prompt_player_action(state, available_directions)
                else:
                    print("\nInvalid input. Please try again.")
            
        elif has_rusty_saw and not has_shiny_saw:
            if has_interacted == False:
                state.scroll_typewriter("""You approach the Abandoned Lumber Camp, the path remains obstructed by the fallen log.""")
                has_interacted = True
            if has_sharpening_stone:
                while True:
                    player_choice = input("\n\nDo you wish to sharpen the Rusty Saw with the Sharpening Stone? (y/n): ").strip().lower()
                    if player_choice == "y":
                        print()
                        state.scroll_typewriter("You successfully sharpen your Saw.")
                        state.remove_from_inventory("Rusty Saw")
                        state.add_to_inventory("Shiny Saw")
                        print("\n\nINVENTORY UPDATED")
                        time.sleep(1)
                        break
                    elif player_choice == "n":
                        print()
                        state.scroll_typewriter("You decide not to sharpen the Rusty Saw.")
                                # ----- Movement or Other Actions -----
                        input("\n\n\nPress enter to continue\n")
                        available_directions = {
                            "south": "Eastern Orchard",
                        }
                        return prompt_player_action(state, available_directions)
                    else:
                        print("\nInvalid input. Please try again.")
            else: # Has rusty saw but no sharpening stone
                if has_interacted == False:
                    state.scroll_typewriter("""You approach the Abandoned Lumber Camp, the path remains obstructed by the fallen log.""")
                    has_interacted = True
                
                while True:    

                    player_choice = input("\n\nDo you wish to use the Rusty Saw on the fallen log? (y/n): ").strip().lower()
                    if player_choice == "y":
                        print()
                        state.scroll_typewriter("You attempt to saw through the fallen log but your saw is not sharp. Your path remains obstructed.")
                                # ----- Movement or Other Actions -----
                        input("\n\n\nPress enter to continue\n")
                        available_directions = {
                            "south": "Eastern Orchard",
                        }
                        return prompt_player_action(state, available_directions)
                    
                    elif player_choice == "n":
                        print()
                        state.scroll_typewriter("You decide not to use the Rusty Saw on the fallen log. Your path remains obstructed.")
                                # ----- Movement or Other Actions -----
                        input("\n\n\nPress enter to continue\n")
                        available_directions = {
                            "south": "Eastern Orchard",
                        }
                        return prompt_player_action(state, available_directions)
                    else:
                        print("\nInvalid input. Please try again.")
            

        elif has_shiny_saw:
            if has_interacted == False:
                state.scroll_typewriter("""You approach the Abandoned Lumber Camp, the path remains obstructed by the fallen log.""")
                has_interacted = True
            while True:
                
                player_choice = input("\n\nDo you wish to use the Shiny Saw on the fallen log? (y/n): ").strip().lower()
                if player_choice == "y":
                    print()
                    state.scroll_typewriter("You successfully saw through the fallen log! Your path to the Abandoned Lumber Camp is now clear.")
                    print()
                    location_state["clear_path"] = True # This updates the world state
                    break # Exit the inner loop, then the main loop condition will be checked
                elif player_choice == "n":
                    print()
                    state.scroll_typewriter("You decide not to use the Shiny Saw on the fallen log. Your path remains obstructed.")
                            # ----- Movement or Other Actions -----
                    input("\n\n\nPress enter to continue\n")
                    available_directions = {
                        "south": "Eastern Orchard",
                    }
                    return prompt_player_action(state, available_directions)
                else:
                    print("\nInvalid input. Please try again.")
        
        # After any action that might change clear_path, re-evaluate it for the next loop iteration
        # The main while loop condition `while not location_state.get("clear_path", False):` will now correctly
        # pick up the change.

    # --- Path is clear, handle subsequent actions ---
    # Re-evaluate has_timber_wagon after the path is clear
    has_timber_wagon = "Timber Wagon" in state.get_inventory()

    if not has_timber_wagon:
        if not visited:
            state.scroll_typewriter("""
You enter the Abandoned Lumber Camp and see rusting tools that lie scattered amidst moss-covered stumps. Your gaze is drawn to a 
large wagon, heavily laden with neatly stacked timber bundles, gleaming faintly in the dappled sunlight.""")
            location_state["visited"] = True
        else:
            state.scroll_typerwriter("""
You return to the Abandoned Lumber Camp and your gaze falls once more upon the large wagon, still heavily laden with its neatly 
stacked timber bundles, patiently waiting in the dappled sunlight.""")
        
        
        while True:
            player_choice = input("\n\nDo you wish to take the Timber Wagon? (y/n): ").strip().lower()
            if player_choice == "y":
                print()
                state.scroll_typewriter("""You successfully take the Timber Wagon!""")
                state.add_to_inventory("Timber Wagon")
                print("\n\nINVENTORY UPDATED")
                    # ----- Movement or Other Actions -----
                input("\n\n\nPress enter to continue\n")
                available_directions = {
                    "south": "Eastern Orchard",
                }
                return prompt_player_action(state, available_directions)
            elif player_choice == "n":
                print()
                state.scroll_typewriter("You decide not to take the Timber Wagon.")
                        # ----- Movement or Other Actions -----
                input("\n\n\nPress enter to continue\n")
                available_directions = {
                    "south": "Eastern Orchard",
                }
                return prompt_player_action(state, available_directions)
                
            else:
                print("\nInvalid input. Please try again.") 
    
    else: # If has_timber_wagon is True
        state.scroll_typewriter("""
You return to the Abandoned Lumber Camp. You see the area where the Timber Wagon once laid.""")

        # ----- Movement or Other Actions -----
        input("\n\n\nPress enter to continue\n")
        available_directions = {
            "south": "Eastern Orchard",
        }
        return prompt_player_action(state, available_directions)

def angel_crossing(state): 
    world_state = state.get_world_state()
    location_state = world_state.get("Angel Crossing", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_timber_wagon = "Timber Wagon" in state.get_inventory()
    clear()
    print(f"Location: Angel Crossing\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    bridge_built = location_state.get("bridge_built", False)
    if not visited:
        if not has_timber_wagon:
            location_state["visited"] = True
            state.scroll_typewriter("""
The roar of the river is deafening as you approach the Broken Bridge, its shattered timbers jutting out like broken teeth over the 
churning water. Standing impatiently on the near bank is Sir Digglescoff, a royal knight in polished armor, flanked by a handful 
of his weary men and panting horses. 

"Blast it all!" he mutters, slamming a gauntleted fist against a broken railing. "Those thieving rascals, they made off with a royal 
armory wagon, then cut the bridge clean to escape! We can't pursue them like this. If only we had some large timbers... enough to 
mend this gap, we'd be after them in a flash!" """)
            if "A Riveting Repair Job" not in quest_titles:
                state.add_quest({
                    "title": "A Riveting Repair Job",
                    "description": "Find enough large timbers to help Sir Digglescoff repair the Broken Bridge.",
                    "status": "Active"
                })
            print("\n\nQUEST LOG UPDATED")
            # ----- Movement or Other Actions -----
            input("\n\n\nPress enter to continue\n")
            available_directions = {
                "west": "Eastern Orchard",
            }
            return prompt_player_action(state, available_directions)
        elif has_timber_wagon:
            location_state["visited"] = True
            state.scroll_typewriter("""
The roar of the river is deafening as you approach the Broken Bridge, its shattered timbers jutting out like broken teeth over the 
churning water. Standing impatiently on the near bank is Sir Digglescoff, a royal knight in polished armor, flanked by a handful 
of his weary men and panting horses. His eyes widen as he spots the large timbers you're carrying. 
                                    
"By the King's beard, you've got them! Excellent! With these, we can mend this bridge and continue our pursuit of those confounded 
bandits. You've just saved the day, adventurer!" 

With swift, coordinated effort, Sir Digglescoff and his men, aided by your timber, quickly set about repairing the bridge. Soon, a 
sturdy, if makeshift, path spans the chasm. The knight claps you firmly on the shoulder. 
                                    
"For your bravery and loyalty to the King's cause, take this!" he declares, pressing a gleaming Loyalist Signet into your hand. 
Then, with a mighty roar that echoes across the water, "For the King! Charge!" he cries, and he and his men gallop across the newly 
mended bridge, disappearing into the distance in pursuit of the fleeing bandits.""")
            if "A Riveting Repair Job" not in quest_titles:
                state.add_quest({
                    "title": "A Riveting Repair Job",
                    "description": "Find enough large timbers to help Sir Digglescoff repair the Broken Bridge.",
                    "status": "Completed"
                })

            state.add_to_inventory("Royal Signet")
            
            state.remove_from_inventory("Timber Wagon")
            print("\n\nQUEST LOG AND INVENTORY UPDATED")
            # ----- Movement or Other Actions -----
            input("\n\n\nPress enter to continue\n")
            available_directions = {
                "east": "Bandit Camp",
                "west": "Eastern Orchard",
            }
            return prompt_player_action(state, available_directions)
    elif not bridge_built and not has_timber_wagon:
        state.scroll_typewriter("""
You return to the Broken Bridge, but the wide, roaring gap remains just as you left it. Sir Digglescoff and his men are still there, 
looking even more impatient, their gazes fixed across the chasm. The knight shakes his head, glancing at the shattered timbers. 
            
"The bandits are getting further and further away with every passing moment! We're stuck here until this bridge is mended. If only 
there were someone who could help us..." """)
        # ----- Movement or Other Actions -----
        input("\n\n\nPress enter to continue\n")
        available_directions = {
            "west": "Eastern Orchard",
        }
        return prompt_player_action(state, available_directions)
    
    elif not bridge_built and has_timber_wagon:
        state.scroll_typewriter("""
You return to the Broken Bridge, but the wide, roaring gap remains just as you left it. Sir Digglescoff and his men are still there, 
looking even more impatient, their gazes fixed across the chasm. The knight shakes his head, glancing at the shattered timbers.
His eyes widen as he spots the large timbers you're carrying. "By the King's beard, you've brought them! Excellent! With these, we 
can mend this bridge and continue our pursuit of those confounded bandits. You've just saved the day, adventurer!"

With swift, coordinated effort, Sir Digglescoff and his men, aided by your timber, quickly set about repairing the bridge. Soon, a 
sturdy, if makeshift, path spans the chasm. The knight claps you firmly on the shoulder. 
                                
"For your bravery and loyalty to the King's cause, take this!" he declares, pressing a gleaming Loyalist Signet into your hand. 
Then, with a mighty roar that echoes across the water, "For the King! Charge!" he cries, and he and his men gallop across the newly 
mended bridge, disappearing into the distance in pursuit of the fleeing bandits.""")
        location_state["bridge_built"] = True
        state.remove_from_inventory("Timber Wagon")
        state.add_to_inventory("Royal Signet")
        state.complete_quest("A Riveting Repair Job")
        print("\n\nQUEST LOG AND INVENTORY UPDATED")
        # ----- Movement or Other Actions -----
        input("\n\nPress enter to continue\n")
        available_directions = {
            "east": "Bandit Camp",
            "west": "Eastern Orchard",
        }
        return prompt_player_action(state, available_directions)
    elif bridge_built:
        state.scroll_typewriter("You return to Angel Crossing, the makeshift repairs still holding the bridge in place.")
        
        # ----- Movement or Other Actions -----
        input("\n\n\nPress enter to continue\n")
        available_directions = {
            "east": "Bandit Camp",
            "west": "Eastern Orchard",
        }
        return prompt_player_action(state, available_directions)

def forest_entrance(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Forest Entrance", {})
    visited = location_state.get("visited", False)
    witch_defeated = location_state.get("witch_defeated", False)
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_staff = "Wizard Staff" in state.get_inventory()
    has_mirror = "Ornate Hand Mirror" in state.get_inventory()
    clear()
    
    print(f"Location: Forest Entrance\n\n")
    if not visited: #If you enter for the first time
        state.scroll_typewriter("""You reach the edge of the woods. You meet Tannenbark, the enchanted squirrel.""")
        location_state["visited"] = True  # Update visited flag
        
    
    elif visited and not has_staff and not witch_defeated: # If enter but don't have the staff
        state.scroll_typewriter("You return to the edge of the woods. Tannenbark is wondering if you really know where you're going.")

    elif visited and has_staff and not witch_defeated: # If enter and do have the staff, encounter the Hag!!!
        state.scroll_typewriter("You return to the edge of the woods. You encounter the Witch! She wants the wizard staff back!")
        print()
        if not has_mirror:
            state.scroll_typewriter(""""Foolish child! You will need something more powerful to match my magic capabilities" She laughs
a very disturbing evil laugh as her bony hand emerges from her shaggy cloak revealing a crooked wand. Before she casts whatever spell she
had in mind, you turn around a flee from the area!""")

        else: 
            state.scroll_typewriter(""""Foolish child! You think you can just take that staff from me?" Before she casts a spell, you run at
the old hag with the mirror in your hand. At first she is startled, then confused, then frantically distressed as she recognizes herself in
the swifly apporaching hand mirror. She screams in terror as she retreats in the woods, yelling something about her mismatched warts and uneven
eyebrows.""")
            location_state["witch_defeated"] = True 

    elif witch_defeated: # If you have already defeated the witch
        state.scroll_typewriter("You return to the edge of the woods. You remember how bravely you defeated the witch.")

    
    
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "Dire Wolf Pines",
        "east": "Twilight Grove",
        "south": "North Gate",
        "west": "Hunter's Cabin"
    }
    return prompt_player_action(state, available_directions)

def abandoned_hut(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Abandoned Hut", {})
    clear()
    print(f"Location: The Abandoned Hut\n\n")

    visited = location_state.get("visited", False)
    if visited:
        state.scroll_typewriter("You enter into the Old Hag's familiar hut.")
    else:
        state.scroll_typewriter("""
You enter into the Old Hag's hut for the first time. Looking around, you find the staff!""")
        state.add_to_inventory("Wizard Staff")

        print("\n\nINVENTORY UPDATED")

    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "west": "Twilight Grove",
    }
    return prompt_player_action(state, available_directions)

def dire_wolf_pines(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Forest Entrance", {})
    not_visited = location_state.get("visited", False)
    has_bow = "Hunting Bow" in state.get_inventory()
    clear()
    
    print(f"Location: Dire Wolf Pines\n\n")
    if not_visited: #If you enter for the first time
        state.scroll_typewriter("""You find yourself in an area with very tall trees. You hear a wolf cry in the distance. And then another one, [pause]closer.
Before you have time to react, there are three, barefanged wolves slowly approaching you, because you are their next meal.""")
        location_state["visited"] = True  # Update visited flag
        input("\n\n\nPress ENTER to continue")
        if has_bow:
            state.scroll_typewriter("""You whip out your hunting bow and quickly release an arrow in each of the wolves chests, each
dropping to the ground. Thank goodness you got the archery merit badge last summer!""")
        else:
            state.scroll_typewriter("""The dire wolves are too swift, their fangs too sharp for close combat. You are forced to flee!""")
            action = "flee"
            return action
    else: # If you have already defeated the wolf pack
        state.scroll_typewriter("You return to the familiar area, where you were attacked by the wolves.")

    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "Hollowpine Outpost",
        "south": "Forest Entrance",
        "west": "Cave Entrance"
    }
    return prompt_player_action(state, available_directions)

def twilight_grove(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Twilight Grove", {})

    clear()
    print(f"Location: Twilight Grove\n\n")

    # Set Flags
    visited = location_state.get("visited", False)
    fountain_visited = location_state.get("fountain", False)

    # First time visiting
    if not visited:
        location_state["visited"] = True
        state.scroll_typewriter("""
You push deeper into the woods, and the trees start getting... weird. Their trunks are now the size of tavern barrels stacked 
in a bear-hug, which, coincidentally, is about what it would take to hug one. You hink of hugging your Aunt Lisa again—if she were 
taller, woodier, and slightly less judgmental. Oh, and still in that scratchy black dress. Darkness and musty fog work together to 
make the forest obviously like it’s not meant to be disturbed. The sunlight agrees anyway.
[pause]
Eventually, you stumble into a clearing—somehow perfectly circular and suspiciously serene. Here, sunlight pierces through in lazy golden 
shafts like it just had to show off for this one spot. In the center sits a small, white marble bowl. It’s not just any bowl—it’s 
fountain-shaped, unnecessarily fancy, and just sitting there like it paid rent. Inside, water remains still and smooth, save for a few 
glowing lights zipping around the surface like they’re late for a fairy rave.
[pause]
You swear one of them just did a loop-de-loop.
[pause]
What do you do?
[pause]
""")
    elif visited:
        state.scroll_typewriter("""You return to the strange part of the woods, where everything seems familiarly unfamiliar. You remember
that the grove was somewhere nearby but it seems to be anywhere but where you look.""")
    # Encounter logic
    if not fountain_visited:
        location_state["fountain"] = True
        while True:
            print("\n\n1. Approach the fountain (What could go wrong with glowing water and implied fae activity?)\n2. Go around the clearing (Because skipping enchanted landmarks always ends well.)")
            action = input("\nACTION: ").strip()

            if action == "1":
                location_state["fountain"] = True
                state.scroll_typewriter("""
You take a cautious step forward. The lights pause their fairy conga line and seem to notice you. One zips up close, hovers near your 
nose, and makes a noise that could be a giggle or a mosquito with a superiority complex.
[pause]
The marble bowl is cooler than expected. Like, suspiciously cool. The kind of cool that says "I have secrets and possibly a sentient 
ecosystem living in me." The water is so clear it looks less like water and more like a window—too perfect, too still. You lean in, 
and your reflection meets your gaze… but then it blinks. Not in sync with you. A slow, deliberate blink, as if it’s watching you.
[pause]
Before you can panic, one of the glowing lights does a graceful dive into the water, sending ripples across the bowl. A sharp ‘DING’ 
rings and your reflection shifts into a vision. Your senses are blurry and it’s hard to make out what you're seeing, and your curiosity 
pulls you in closer. The light in the corner of your eyes dims as you become completely focused on the surface of the water. 
[pause]""")
                input("Press ENTER to continue")
                print()           
                state.scroll_typewriter("""Suddenly, a green image appears in view, and as you focus, you realize it is three apple trees. Interesting…
The image disappears and is replaced with a glowing key that has a golden tag hanging from it. 
[pause]
You make out a few letters: [pause]A[pause]P[pause]P[pause]L[pause]E[pause]S
[pause]
The image vanishes and you see the forest landscape tilted sideways, as if you had fallen to the forest floor. Oh wait, you did.
[pause]
You pick yourself up and dust off your pants.
[pause]
You feel an odd sense of clarity… and also like you may now owe a favor to an unknown woodland entity.[pause]""")
                break
            elif action == "2":
                state.scroll_typewriter("""
You decide not to trust the glowing bowl of water in the suspiciously perfect clearing—because you’ve read enough cautionary tales to 
know that glowing things in ancient woods rarely hand out cupcakes.
[pause]
Skirting the edge of the trees like you’re avoiding eye contact at a family reunion, you press on into the underbrush. It scratches at 
your legs like nature’s passive-aggressive reminder that you’ve made a choice. The glowing lights behind you seem to huddle together, 
confused, like you just skipped a vital plot point.[pause]
""")
                break
            else:
                print("Invalid choice. Try again.")
                time.sleep(2)
                clear()
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "The Barren Ridge (Under Construction)",
        "east": "Abandoned Hut",
        "west": "Forest Entrance"
    }
    return prompt_player_action(state, available_directions)
#under construction
def hunters_cabin(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Hunter's Cabin", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_evelyn = "Evelyn" in state.get_inventory()
    clear()
    
    print(f"Location: Hunter's Cabin\n\n")
    if not location_state.get("visited", False): #If you enter for the first time
        state.scroll_typewriter("""
You step into the Hunter's Cabin. You meet Lordisk the Hunter and his wife Mallory. 
Their daughter was kidnapped by Phantom and taken to a cave! They plead with you to 
find her and return her safely to them.""")
        location_state["visited"] = True  # Update visited flag
        # Handle Quest giving below
        if "Save Evelyn" not in quest_titles:
            state.add_quest({
                "title": "Save Evelyn",
                "description": "Lordrisk the Hunter needs your help to save his daughter.",
                "status": "Active"
            })
            # Lordrisk offers you a sword.
            print("\n\nQUEST LOG UPDATED")
            
    
    elif location_state.get("visited", True) and has_evelyn: # If you return having completed the quest
        state.scroll_typewriter("""
You enter into the cabin and Evelyn runs into her parents arms. What a sweet reunion.
Lordrisk the Hunter offers to give you a hand any time his skill sets are needed.""")
        state.complete_quest("Remembering The Sacred Order")
        state.add_to_inventory("Health Potion")
        print("\n\nQUEST LOG AND INVENTORY UPDATED")
        input("Press ENTER to continue")
        
        state.scroll_typewriter("Earl then looks to you with deep devotion and loyalty and states that for your service, he will acompany you!")
        print("COMPANIONS UPDATED")
        #state.add_companion({
        #    "title": "Earl the Hallowed Knight",
        #    "description": "A devout soldier who follows you for the great service done to the Windshire Chapels",
        #})
    else: # If you return without completing the quest
        state.scroll_typewriter("""
You pass by the cabin hoping one day you will see this family reunited once more.""")
        
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "Cave Entrance",
        "east": "Forest Entrance",
    }
    return prompt_player_action(state, available_directions)

def cave_entrance(state):
    world_state = state.get_world_state()
    location_state = world_state.get("Cave Entrance", {})
    clear()
    
    print(f"Location: Cave Entrance\n\n")
    if not location_state.get("visited", False): #If you enter for the first time
        state.scroll_typewriter("""
You hike to the cave entrance. You hear a menacing howl coming from inside the cave. You also see a little 
teddybear abandoned at the entrance.""")
        location_state["visited"] = True  # Update visited flag
    
    elif location_state.get("visited", True):
        state.scroll_typewriter("""
You approach the familiar cave entrance.""")
    
    # ----- Movement or Other Actions -----
    input("\n\n\nPress enter to continue\n")
    available_directions = {
        "north": "The Tunnels",
        "east": "Dire Wolf Pines",
        "south": "Hunter's Cabin",
    }
    return prompt_player_action(state, available_directions)

def the_tunnels(state):
    world_state = state.get_world_state()
    location_state = world_state.get("The Tunnels", {})
    quest_log = state.get_quest_log()
    quest_titles = [q["title"] for q in quest_log]
    has_evelyn = "Evelyn" in state.get_inventory()
    clear()
    
    print(f"Location: The Tunnels\n\n")




# GAME LOOP
def game_loop():

    state = GameState()
    

    while True:
        
        clear()
        load_game = run_game_title_menu(state)
        if load_game:
            run = True
        else:
            break
        clear()
        
        while run:
            location = state.get_location()
            action = None
            

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
                    state.set_location("the_gallows")
                elif action == "east":
                    print("You go East")
                    time.sleep(1)
                    state.set_location("east_gate")
                elif action == "apples":
                    print("A secret hatch opens inside the fountain!")
                    time.sleep(1)
                    pass # ADD SECRET HERE!
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
            
            elif location == "bazaar":
                action = bazaar(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("town_center")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("the_graveyard")
                    elif action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("northern_streets")
                    elif action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("the_barracks")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "the_croftward":
                action = the_croftward(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("town_center")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("wizard_tower")
                    elif action == "west":
                        print("You go West")
                        state.set_location("the_graveyard")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
            
            elif location == "angel_crossing":
                action = angel_crossing(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("eastern_orchard")
                    elif action == "east":
                        print("You can't go that way")
                        #handle logic for if the player has lumber to repair the bridge
                        pass

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "abandoned_lumber_camp":
                action = abandoned_lumber_camp(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("eastern_orchard")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "wizard_tower":
                action = wizard_tower(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("the_croftward")
                    
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "the_gallows":
                action = the_gallows(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("town_center")
                    elif action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("northern_streets")
                    
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "northern_streets":
                action = northern_streets(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("north_gate")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("the_gallows")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("bazaar")
                    elif action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("city_hall")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "city_hall":
                action = city_hall(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("northern_streets")
                    
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "the_barracks":
                action = the_barracks(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("bazaar")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("south_west_gate")
                    elif action == "west":
                        print("You go West")
                        state.set_location("the_keep_entrance")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "the_keep_entrance":
                action = the_keep_entrance(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("the_barracks")
                    elif action == "west":
                        favor_for_flavor_completed = state.is_quest_completed("A Favor for Flavor")
                        if favor_for_flavor_completed:
                            print("You go west into the Keep")
                            time.sleep(1)
                            state.set_location("the_banquet")
                        else:
                            print("You can't go that way yet.")
                            time.sleep(1)
                    
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "east_gate":
                action = east_gate(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("eastern_orchard")
                    elif action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("town_center")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "south_west_gate":
                action = south_west_gate(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("the_barracks")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("southern_outskirts")
                    elif action == "west":
                        print("You go West")
                        state.set_location("windshire_chapels")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
            elif location == "north_gate":
                action = north_gate(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        has_signet = "Royal Signet" in state.get_inventory() # See if the player can get past the guards
                        if has_signet:
                            print("You go North")
                            time.sleep(1)
                            state.set_location("forest_entrance")
                        else:
                            print("You can't go that way.")

                    elif action == "south":
                        print("You go South")
                        state.set_location("northern_streets")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "eastern_orchard":
                action = eastern_orchard(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("abandoned_lumber_camp")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("angel_crossing")
                    elif action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("east_gate")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "windshire_chapels":
                action = windshire_chapels(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("south_west_gate")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "the_graveyard":
                action = the_graveyard(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("bazaar")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("the_croftward")

                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "forest_entrance":
                action = forest_entrance(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("hunters_cabin")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("north_gate")
                    elif action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("dire_wolf_pines")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("twilight_grove")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "abandoned_hut":
                action = abandoned_hut(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("twilight_grove")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "dire_wolf_pines":
                action = dire_wolf_pines(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("forest_entrance")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "twilight_grove":
                action = twilight_grove(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "west":
                        print("You go West")
                        time.sleep(1)
                        state.set_location("forest_entrance")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
            
            elif location == "hunters_cabin":
                action = hunters_cabin(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("cave_entrance")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("forest_entrance")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
            
            elif location == "cave_entrance":
                action = cave_entrance(state)

                if action in ["north", "south", "east", "west"]:
                    # You can define your own map transition logic here
                    if action == "north":
                        print("You go North")
                        time.sleep(1)
                        state.set_location("the_tunnels")
                    elif action == "east":
                        print("You go East")
                        time.sleep(1)
                        state.set_location("dire_wolf_pines")
                    elif action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("hunters_cabin")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
                elif action == "flee":
                    print("You flee!")
                    time.sleep(1)
                    state.set_location("twilight_grove")
                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False

            elif location == "the_tunnels":
                action = the_tunnels(state)
                if action in ["north", "south", "east", "west"]:
                    if action == "south":
                        print("You go South")
                        time.sleep(1)
                        state.set_location("cave_entrance")
                if action == "quit":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
                elif action == "flee":
                    print("You flee!")
                    time.sleep(1)
                    state.set_location("twilight_grove")
                elif action =="death":
                    print("Exiting the game...")
                    time.sleep(1)
                    run = False
            else:
                print(f"Unknown location: {location}")
                run = False



# Run the game please
game_loop()
