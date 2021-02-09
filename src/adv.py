from room import Room
from player import Player
from item import Item

import random
from fuzzywuzzy import fuzz, process

# Declare all the rooms

input_possibilities = {
    "movement": {
        "north_movement": ["north"],
        "south_movement": ["south"],
        "east_movement": ["east"],
        "west_movement": ["west"]
    },
    "actions": {
        "observation": ["look", "see", "find"],
        "acquire": ["get", "pick up", "acquire", "grab"],
        "items": ["item", "inventory", "holding", "backpack"],
        "drop": ["drop", "throw", "remove", "let go"]
    }
}

rooms = {
    'outside': Room("Outside Cave Entrance",
                    "North of you, the cave mount beckons"),

    'foyer': Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow': Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

# Link rooms together

rooms['outside'].n_to = rooms['foyer']
rooms['foyer'].s_to = rooms['outside']
rooms['foyer'].n_to = rooms['overlook']
rooms['foyer'].e_to = rooms['narrow']
rooms['overlook'].s_to = rooms['foyer']
rooms['narrow'].w_to = rooms['foyer']
rooms['narrow'].n_to = rooms['treasure']
rooms['treasure'].s_to = rooms['narrow']

#
# Main
#


def fill_rooms_with_items():
    base_name = [
        "Staff",
        "Rapier",
        "Longsword",
        "Wand",
        "Dagger",
        "Helmet",
        "Breastplate",
        "Boots",
        "Leggings"]
    descriptors = [
        "Holding",
        "Resistance",
        "Luck",
        "Power",
        "Fun",
        "Destruction"]
    descriptions = [
        "It can shoot a fireball, but it's not strong enough to do anything but light a candle.",
        "It is very pretty looking, but not very effective.",
        "It's covered in rust and looks very worn out, but it can still be used effectively."]

    for room in rooms:
        item_name = random.choice(base_name) + " of " + \
            random.choice(descriptors)
        item = Item(item_name, random.choice(descriptions))
        rooms[room].items.append(item)


def filter_user_input(user_input):
    filtered_input = user_input.lower().strip()

    if filtered_input == "quit" or filtered_input == "q":
        print("Thanks for playing! See you next time!")
        exit(0)
    elif filtered_input == "help":
        print("Try typing a certain direction or looking around.")
        return 0
    elif filtered_input == "n":
        return "north"
    elif filtered_input == "s":
        return "south"
    elif filtered_input == "w":
        return "west"
    elif filtered_input == "e":
        return "east"
    else:
        return filtered_input


def move_player(direction):
    if direction == "north" or direction == "up":
        try:
            current_player.room = current_player.room.n_to
            print("Heading north")
        except AttributeError:
            print("There is no room to the north.")
    elif direction == "south" or direction == "down":
        try:
            current_player.room = current_player.room.s_to
            print("Heading south")
        except AttributeError:
            print("There is no room to the south.")
    elif direction == "east" or direction == "right":
        try:
            current_player.room = current_player.room.e_to
            print("Heading east")
        except AttributeError:
            print("There is no room to the east.")
    elif direction == "west" or direction == "left":
        try:
            current_player.room = current_player.room.w_to
            print("Heading west")
        except AttributeError:
            print("There is no room to the west.")


def observe_room():
    if len(current_player.room.items) == 0:
        print("You find nothing in the room.")
        return
    for item in current_player.room.items:
        print(f"You see a {item.name}")


def get_item():
    if len(current_player.room.items) == 0:
        print("There is nothing in the room to get.")
        return
    # Add a check if there are multiple items and ask for which item to get or see if the user supplied it
    # Use that check to remove and add the specific item, for now there is
    # only one item per room
    item = current_player.room.items.pop(0)
    current_player.items.append(item)
    print(f"You put the {item.name} in your backpack.")


def drop_item(item_string):
    for held_item in current_player.items:
        print(fuzz.token_set_ratio(item_string, held_item.name))
        if fuzz.token_set_ratio(item_string, held_item.name) > 60:
            current_player.items.remove(held_item)
            current_player.room.items.append(held_item)
            print(f"You dropped the {held_item.name}")
            return
    print(f"You don't have that item. Try being more specific.")


def view_inventory():
    if len(current_player.items) == 0:
        print("You have no items.")
        return
    for item in current_player.items:
        print(item)


def check_user_input(user_input):
    if user_input == 0:
        return
    global input_possibilities
    ratios = []
    for dictionary in input_possibilities:
        for sub_dictionary in input_possibilities[dictionary]:
            highest_ratio = process.extractOne(
                user_input,
                input_possibilities[dictionary][sub_dictionary],
                scorer=fuzz.token_set_ratio)
            ratios.append(highest_ratio)
    ratios.sort(key=lambda x: x[1], reverse=True)
    highest_ratio = ratios[0]

    if highest_ratio[1] < 80:
        print("I'm not sure what you're trying to do.")
        return

    for direction in input_possibilities["movement"]:
        if highest_ratio[0] in input_possibilities["movement"][direction]:
            move_player(highest_ratio[0])
            return

    if highest_ratio[0] in input_possibilities["actions"]["observation"]:
        observe_room()
        return
    elif highest_ratio[0] in input_possibilities["actions"]["acquire"]:
        get_item()
        return
    elif highest_ratio[0] in input_possibilities["actions"]["items"]:
        view_inventory()
        return
    elif highest_ratio[0] in input_possibilities["actions"]["drop"]:
        drop_item(user_input)


# Make a new player object that is currently in the 'outside' room.


character_name = filter_user_input(input("What is your name?\n"))
current_player = Player(character_name, rooms['outside'])

print(
    f"Welcome {current_player.name.capitalize()}! You shall now begin you're adventure!\
 Type quit at anytime to leave and type help if you aren't sure what to do.\n\n")

fill_rooms_with_items()

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

while True:
    print(current_player.room)

    check_user_input(
        filter_user_input(
            input("\033[94m\nWhat do you want to do?\n")))
