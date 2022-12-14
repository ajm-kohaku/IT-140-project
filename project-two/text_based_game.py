'''
# Amber Murphy
# IT-140: 22EW22
# Module 7: TextBasedGame
uses match statement for decision making
'''
import collections
import json
import os
import sys
import time
import re


class GameStats:
    '''Global variables for the game.'''

    def __init__(self):
        self.inventory = ['Turtle', 'Dragon', 'Bird', 'Tiger']
        self.tokens = ['Turtle', 'Dragon', 'Bird', 'Tiger']
        self.win_inventory = ['Sword', 'Talisman', 'Manuscript']
        self.can_win = False
        self.exit = False
        self.start = True
        self.current_room = 'murasakiResidence'
        self.selected_option = ''
        self.has_bad_input = False
        self.game_data = {}


gamer = GameStats()
DECORATIVE_TEXT = '.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ.:｡+ﾟﾟ+｡:.ﾟ'


def intro_text():
    '''Create introduction text to the game.'''
    # pylint: disable=line-too-long
    return ('\n     WELCOME TO ONMYOJI!\n'
            '\n You are a young Onmyoudou practitioner in the late Heian Period of Japan. Time is running out to stop the emergence of the Great Serpent.'
            '\n The city\'s magical array needs to be activated to prevent the Serpent from fully manifesting and destroying the city.'
            '\n You must activate the array by placing these four tokens at shrines positioned around the city and obtaining 3 items to complete the ritual to seal the beast.'
            '\n You must hurry, the Serpent is already manifesting and the city is in danger! '
            '\n Each shrine has a statue of the Guardian God that protects that cardinal direction. '
            '\n Give the turtle token to Genbu, the Dragon token to Seiyruu, the Bird token to Suzaku, and the Tiger token to Byakko.'
            '\n Good luck! And may the spirits protect you!'
            )


def instruction_text():
    '''Create instruction text for the game.'''
    # pylint: disable=line-too-long
    return ('\n\nInstructions:'
            '\n To move to a different location, type: "go " followed by direction provided in the options.'
            '\n To place an item at a shrine, type: "place " followed by the name of the item you want to leave behind.'
            '\n To get an item from a location, type: "get " followed by the name of the item you want to retrieve.'
            '\n To prematurely exit the game, type: "Exit".'
            '\n None of these options are case sensitive.'
            '\n Type "Help" to see these instructions again.'
            )


def can_win():
    '''determine if gamer can win the game right now
        * update gamer.can_win
        * print out text if the player hasn't seen it yet.
    '''
    win_is_met = collections.Counter(
        gamer.inventory) == collections.Counter(gamer.win_inventory)
    # pylint: disable=line-too-long
    can_win_text = 'You have all you need to defeat the Great Serpent. Head to the Palace post-haste!\n'
    if win_is_met and not gamer.can_win:
        typewriter_output(f'{can_win_text}\n')
    elif win_is_met and gamer.can_win:
        print(can_win_text)
    return win_is_met


def boss_room():
    '''Handle boss room scenario'''
    typewriter_output(gamer.game_data.get('grandPalace').get('description'))
    if gamer.can_win:
     # pylint: disable=line-too-long
        game_over_text = ('\nYes! You have come prepared to meet the Great Serpent.'
                          '\nAs the figure approaches, you raise Totsuka-no-Tsurugi in one hand, the Ofuda Talisman in the other hand.'
                          '\nYou chant the ritual words taught to you by Seimei in the manuscript. The Serpent recoils. You feel the strength of the city\'s array empower you.'
                          '\nThe serpent screams. Black mist spills out out of the figure as it collapses. The mist dissipates harmlessly.'
                          '\nThe skies clear and you catch a glimpse of the array in the sky before it too vanishes.\n'
                          '\n YOU WIN!!')
        typewriter_output(game_over_text)
    else:
        typewriter_output('\nNo. You were not prepared.')
        if any(item in gamer.tokens for item in gamer.inventory):
            game_over_text = ('\nYou were unable to complete the magical array around the city. The Great Serpent forms before you, the skys turn black.'
                              '\nDarkness consumes you. And the last sounds you hear are a sinister laughter.'
                              '\n GAME OVER\n')
            typewriter_output(game_over_text)
        else:
            game_over_text = ('\nYou were able to get the array up in time. However, you were unable to gather all the ritual instruments needed to seal the beast.'
                              '\nThe Great Serpent forms before you, the skys turn black.'
                              '\nDarkness consumes you. And the last sounds you hear are a sinister laughter.'
                              '\n GAME OVER\n')
            typewriter_output(game_over_text)
    gamer.exit = True


def exit_game():
    '''write out game exit and set status to close the game'''
    typewriter_output('Exiting the game. Goodbye!')
    gamer.exit = True


def game_help():
    '''reprint game help text. add sleep to keep text up a bit longer'''
    typewriter_output(instruction_text(), 0.01)
    time.sleep(1)
    gamer.has_bad_input = False


def move(option: str):
    '''handle moving to different areas mechanic'''
    directions: dict = gamer.game_data.get(
        gamer.current_room).get('directions')
    if option.lower() in directions.keys():
        gamer.current_room = directions.get(option.lower())
        gamer.has_bad_input = False
    else:
        gamer.has_bad_input = True


def get_item(item: str):
    '''handle getting an item mechanic'''
    item = item.title()
    current_room: dict = gamer.game_data.get(gamer.current_room)
    if (current_room.get('item') and current_room.get('item') == item
            and current_room.get('item') not in gamer.inventory):

        typewriter_output(current_room.get('itemDescription'))
        gamer.inventory.append(current_room.get('item'))
        gamer.game_data.get(gamer.current_room)['item'] = ''
        gamer.has_bad_input = False

    elif (current_room.get('item') and current_room.get('item') == item
            and current_room.get('item') in gamer.inventory):
        # pylint: disable=line-too-long
        oops_text = (
            f'Well that\'s embarrassing. It looks like {item} is already in your inventory. Let\'s fix that up... there.. all set!')
        typewriter_output(oops_text)
        gamer.game_data.get(gamer.current_room)['item'] = ''
        gamer.has_bad_input = False

    else:
        gamer.has_bad_input = True


def place_token(item: str):
    '''handle placing a token mechanic'''
    current_room = gamer.game_data.get(gamer.current_room)
    if (current_room.get('token') and current_room.get('token') == item.title()
            and current_room.get('token') in gamer.inventory):

        typewriter_output(current_room.get('tokenDescription'))
        gamer.inventory.remove(item.title())
        gamer.game_data.get(gamer.current_room)['item'] = item.title()
        gamer.has_bad_input = False

    elif (current_room.get('token') and current_room.get('token') == item.title()
            and current_room.get('token') not in gamer.inventory):

        typewriter_output(f'The {item} is not currently in your inventory')
        gamer.has_bad_input = False

    elif current_room.get('token') and current_room.get('token') in gamer.inventory:
        typewriter_output(current_room.get('wrongTokenDescription'))
        gamer.inventory.remove(item.title())
        gamer.game_data.get(gamer.current_room)['item'] = item.title()
        gamer.has_bad_input = False

    else:
        gamer.has_bad_input = True


def print_gamer_inventory():
    '''print out the current inventory'''
    print('\n\n  Your current inventory:'
          f'\n  {gamer.inventory}'
          '\n')


def current_room_options(room):
    '''return a list of options for the current room'''
    room_dict = gamer.game_data.get(room)
    options = ['']
    for direction in room_dict.get('directions').keys():
        options.append(f'Go {direction.title()}')
    if room_dict.get('token') and room_dict.get('item') == '':
        options.append(f'Place {room_dict.get("token")}')
    if room_dict.get('item'):
        options.append(f'Get {room_dict.get("item")}')
    options.append(
        'Intro (you may need to scroll up to see the text repeated)')
    options.append('Help')
    options.append('Exit')
    return '\n\t\t'.join(options)


def room_text(room: str):
    '''return the text for the current room'''
    gamer.can_win = can_win()
    text = ' '
    if gamer.start:
        text = (f'You begin at the {get_pretty_name(room)}'
                f'\n{gamer.game_data.get(room).get("startDescription")}')
        gamer.start = False
    else:
        text = (f'You have arrived at the {get_pretty_name(room)}.'
                f'\n{gamer.game_data.get(gamer.current_room).get("description")}')
    if gamer.current_room != 'grandPalace':
        text = (f'{text}'
                '\nWhat would you like to do?\nYour options are:'
                f'{current_room_options(room)}\n')
    if gamer.has_bad_input:
        text = f'{text}\n Invalid option. Try again.\n\n'

    return f'{text}\n*> '


def invalid_option(option: str):
    '''handle invalid option'''
    print(f'[{option}] is an invalid option. please try again')


def get_pretty_name(text: str):
    '''return a pretty name for the room'''
    name = text[0].upper() + text[1:]
    name_list = re.findall('[A-Z][^A-Z]*', name)
    return ' '.join(name_list)


def load_game_data():
    '''load the game data from the json file'''
    filename = 'game-data.json'
    if not os.path.exists(filename):
        print(f'File: {filename} does not exist.')
        sys.exit(1)

    with open(filename, encoding="utf-8") as json_file:
        return json.load(json_file)


def typewriter_output(text, speed=0.03):
    '''print out text with a typewriter effect'''
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


def main():
    '''main function'''
    gamer.game_data = load_game_data()
    typewriter_output(intro_text(), speed=0.02)
    print(DECORATIVE_TEXT)
    print(instruction_text())

    while gamer.exit is False:
        print_gamer_inventory()
        gamer_input = str(input(room_text(gamer.current_room)))

        match gamer_input.lower().split():
            case ['go', direction]:
                move(direction)
            case ['place', item]:
                place_token(item)
            case ['get', item]:
                get_item(item)
            case ['help']:
                typewriter_output(instruction_text(), speed=0.01)
                time.sleep(1)
            case ['intro']:
                typewriter_output(intro_text(),speed=0.01)
                time.sleep(1)
            case ['exit']:
                exit_game()
            case _:
                gamer.has_bad_input = True

        if gamer.current_room == 'grandPalace':
            boss_room()

main()
