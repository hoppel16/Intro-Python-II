from room import Room
from player import Player

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
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


def filter_user_input(user_input):
    if user_input == "quit" or user_input == "q":
        print("Thanks for playing! See you next time!")
        exit(0)
    else:
        return user_input.strip().lower()


def check_user_input(user_input):
    if "north" in user_input or user_input == "n":
        print("Heading north")
        try:
            current_player.room = current_player.room.n_to
        except AttributeError:
            print("There is no room to the north.")
    elif "south" in user_input or user_input == "s":
        print("Heading south")
        try:
            current_player.room = current_player.room.s_to
        except AttributeError:
            print("There is no room to the south.")
    elif "east" in user_input or user_input == "e":
        print("Heading east")
        try:
            current_player.room = current_player.room.e_to
        except AttributeError:
            print("There is no room to the east.")
    elif "west" in user_input or user_input == "w":
        print("Heading west")
        try:
            current_player.room = current_player.room.w_to
        except AttributeError:
            print("There is no room to the west.")
    else:
        print("I don't understand.")

# Make a new player object that is currently in the 'outside' room.


character_name = filter_user_input(input("What is your name?\n"))
current_player = Player(character_name, room['outside'])

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

    check_user_input(filter_user_input(input("\033[94mWhat do you want to do?\n")))
