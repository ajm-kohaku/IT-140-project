'''
Amber Murphy
IT-140: 22EW22
Module 6: Module Six Milestone - Move between rooms
'''
# A dictionary for the simplified dragon text game
# The dictionary links a room to other rooms.
rooms = {
    'Great Hall': {'South': 'Bedroom'},
    'Bedroom': {'North': 'Great Hall', 'East': 'Cellar'},
    'Cellar': {'West': 'Bedroom'}
}

# text instructions for the game
def text_instructions():
    return ('\n\nInstructions:\n'
            'Type the direction you want to go.\n'
            'e.g. If your options are North, South, Exit; type South followed by the "Enter" or "Return" key to move in that direction.\n'
            'Type Exit to leave the game.\n'
            'Type Help to see these instructions again.\n')


# get the current room options
def current_room_options(room):
    options = ['']
    for direction in rooms.get(room).keys():
        options.append(direction)
    options.append('Exit')
    return '\n  '.join(options)

# generate the text to display for the current room
def room_text(room, hasBadInput=False):
    room_text = (f'{text_instructions()}\n'
            f'You are currently in the {room}. Where would you like to go?'
            '\nYour options are:'
            f'{current_room_options(room)}\n')
            
    # if the user typed an invalid option, show the error message
    if hasBadInput:
        room_text = f'{room_text}\n Invalid option. Try again.\n\n'
    return room_text


def main():
    # start the game in the Great Hall
    current_room = 'Great Hall'
    hasBadInput = False

    # loop until the user types Exit
    while True:
        # get the user's option
        option = str(input(room_text(current_room, hasBadInput)))

        # check the user's option
        if option.title() == 'Exit':
            print('Taking you to the exit. Goodbye!')
            break
        # if the user types Help, show the instructions
        elif option.title() == 'Help':
            hasBadInput = False
        # if the user types a valid direction, move to that room
        elif option.title() in rooms.get(current_room).keys():
            current_room = rooms.get(current_room).get(option.title())
            hasBadInput = False
        # if the user types an invalid direction, show the instructions with the error message
        else:
            hasBadInput = True
main()
