# 人狼の上限
def maximum_wolf(number_of_player):
    if number_of_player <= 6:
        return 1
    elif number_of_player <= 9:
        return 2
    elif number_of_player <= 14:
        return 3
    elif number_of_player <= 21:
        return 4
    elif number_of_player <= 30:
        return 5
    elif number_of_player <= 41:
        return 6
    elif number_of_player <= 54:
        return 7
    elif number_of_player <= 69:
        return 8
    elif number_of_player <= 86:
        return 9


# 預言者の上限
def maximum_seer(number_of_player):
    if number_of_player <= 6:
        return 1
    elif number_of_player <= 12:
        return 2
    elif number_of_player <= 21:
        return 3
    elif number_of_player <= 33:
        return 4
    elif number_of_player <= 48:
        return 5
    elif number_of_player <= 66:
        return 6
    elif number_of_player <= 87:
        return 7


# 狂人
def maximum_maniac(number_of_player):
    if number_of_player <= 6:
        return 1
    elif number_of_player <= 9:
        return 2
    elif number_of_player <= 12:
        return 3
    elif number_of_player <= 17:
        return 4
    elif number_of_player <= 23:
        return 5
    elif number_of_player <= 30:
        return 6
    elif number_of_player <= 38:
        return 7
    elif number_of_player <= 47:
        return 8
    elif number_of_player <= 57:
        return 9
    elif number_of_player <= 68:
        return 10
