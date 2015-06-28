# Rock-paper-scissors-lizard-Spock
# By Jonathan 0.

import random
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
def valid_names():
    """
    valid_names!
    :return: a dictionary with valid keys and values for each valid key!
    """
    return {'rock': 0, 'spock': 1, 'paper': 2, 'lizard': 3, 'scissors': 4}

def name_to_number(name):
    """
    converts name into numeric value
    :param name:
    :return: key for math otherwise -1 for error
    """
    match_found = -1
    for key in valid_names().keys():  # if no match whoops! invalid key entered by client!
        if key == name:               # only reason this is done, to ensure name is in valid format for key in hash
            match_found = valid_names()[key]
            break
    return match_found

def number_to_name(number):
    """
    number_to_name
    :param number:
    :return: valid name at index otherwise false
    """
    if (number >= 0) and (number < len(valid_names().keys())):
        for key in valid_names().keys():
            if number == valid_names()[key]:
                return key
    else:
        return ''

# 0 - rock      - beats counter clockwise (4, 3) looses with (1, 2)
# 1 - spock     - beats counter clockwise (0, 4) looses with (2, 3)
# 2 - paper     - beats counter clockwise (1, 0) looses with (3, 4)
# 3 - lizard    - beats counter clockwise (2, 1) looses with (4, 0)
# 4 - scissors  - beats counter clockwise (3, 2) looses with (0, 1)
def rpsls(player_choice):
    """
    game implementation
    :param player_choice:
    :return:
    """
    formatted_player_choice = player_choice.lower()
    print '\nPlayer chooses ' + formatted_player_choice
    player_choose_int = name_to_number(formatted_player_choice) # player_cval player's choice translated from dic to #

    ## validate client entry ##
    if player_choose_int < 0:
        print "Say whaaa!? not a valid choice!"
        return None

    ## otherwise! determine CPU choice
    MAX_VALID_CHOICES = len(valid_names().keys())
    cpu_choose_int = random.randrange(0, MAX_VALID_CHOICES)
    cpu_choice = number_to_name(cpu_choose_int)
    if len(cpu_choice):
        print 'Computer chooses ' + cpu_choice

        # calculating tie here to avoid computations
        if cpu_choose_int == player_choose_int:
            print 'Player and computer tie!'
            return None

        ### compute winner ###
        diff = player_choose_int - cpu_choose_int
        if diff < 0:
            diff %= 5
        if diff < 3:
            print 'Player wins!'
        else:
            print 'Computer wins!'

    ## program ends ...
    return None

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls('rock')
rpsls('Spock')
rpsls('paper')
rpsls('lizard')
rpsls('scissors')

# always remember to check your completed program against the grading rubric




