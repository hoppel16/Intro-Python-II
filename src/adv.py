from room import Room
from player import Player
from fuzzywuzzy import fuzz, process

# Declare all the rooms

movement = {
    "north_movement": ["north", "up"],
    "south_movement": ["south", "down"],
    "east_movement": ["east", "right"],
    "west_movement": ["west", "left"]
}

room = {
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

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#


def fill_rooms_with_items():
    


def filter_user_input(user_input):
    filtered_input = user_input.lower().strip()

    if filtered_input == "quit" or filtered_input == "q":
        print("Thanks for playing! See you next time!")
        exit(0)
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


def check_user_input(user_input):
    global movement
    ratios = []
    for dictionary in movement:
        highest_ratio = process.extractOne(
            user_input,
            movement[dictionary],
            scorer=fuzz.token_set_ratio)
        ratios.append(highest_ratio)
    ratios.sort()
    highest_ratio = ratios[0]

    if highest_ratio[1] < 80:
        print("I'm not sure what you're trying to do.")
        return

    if highest_ratio[0] == "north" or highest_ratio[0] == "up" or highest_ratio[0] == "forward":
        try:
            current_player.room = current_player.room.n_to
            print("Heading north")
        except AttributeError:
            print("There is no room to the north.")
    elif highest_ratio[0] == "south" or highest_ratio[0] == "down" or highest_ratio[0] == "backward":
        try:
            current_player.room = current_player.room.s_to
            print("Heading south")
        except AttributeError:
            print("There is no room to the south.")
    elif highest_ratio[0] == "east" or highest_ratio[0] == "right":
        try:
            current_player.room = current_player.room.e_to
            print("Heading east")
        except AttributeError:
            print("There is no room to the east.")
    elif highest_ratio[0] == "west" or highest_ratio[0] == "left":
        try:
            current_player.room = current_player.room.w_to
            print("Heading west")
        except AttributeError:
            print("There is no room to the west.")

# Make a new player object that is currently in the 'outside' room.


character_name = filter_user_input(input("What is your name?\n"))
current_player = Player(character_name, room['outside'])

print(f"Welcome {current_player.name}! You shall now begin you're adventure! Type quit at anytime to leave.\n\n")

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
