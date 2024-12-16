import os

import random, statistics

import display_log as log, role_limit as limit


terminal_width = os.get_terminal_size().columns

# _____________________________________________________________________________________________________________________
# list宣言

# player list
player_list = []

# role別に保存
villager = []
wolf = []
seer = []
maniac = []
role_dict = {}

# 生存人数
current_player = []
current_wolf = []  # 人狼陣営
current_villager = []  # 市民陣営

# 表示用
dis_current_total_player = []
dis_current_villager = []  # 狂人含む
dis_current_wolf = []  # 人狼のみ

# role別の動作用
can_seer_list = []
killed_list = []
kill_possible = []
vote = []

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\||||||||||||||||||||||||||||||||||||||||||||||
# ゲーム進行で使うもの(list以外)

# player人数
num_of_player = int()

timeslot = str()  # 時間帯表示("role check" + 昼/夜)
remplayer = {}


# player情報 [ Wolf : x , Villager : y , Total : z]
def rem():
    global remplayer
    remplayer = {
        "Wolf": len(dis_current_wolf),
        "Villager": len(dis_current_villager),
        "Total": len(current_player),
    }

    return remplayer


# listをstrに変換( Only [len(list) == 1] )
def tally(exile):

    if len(exile) == 1:

        for i in exile:
            return i


# colorと値
color_dict = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",  # 色リセット用
}


# 色つけて出力
def print_color(text, color="red"):
    print(color_dict[color] + text + color_dict["reset"], end="")


# コマンドクリア
def echooff():
    os.system("clear")
    print(o_detail(timeslot, rem()))


# 詳細を返す
def o_detail(timeslot, rem1):
    detail = f"[ {timeslot} ] [ {color_dict["red"]}Wolf : {rem1["Wolf"]}{color_dict["reset"]} , {color_dict["green"]}Villager : {rem1["Villager"]}{color_dict["reset"]} , Total : {rem1["Total"]}]"
    return detail


# _____________________________________________________________________________________________________________________
# ゲーム初期設定


# プレイヤー数、名前を取得
def get_player_names():
    global player_list, num_of_player, villager, current_player

    while True:
        try:
            num_of_player = int(input("Enter the number of players: "))

            if num_of_player >= 4:
                log.start.number_of_player(num_of_player)
                break

            else:
                print("This game can't be played with less than 3 people.")

        except ValueError:
            print("Please enter a valid number.")

    for i in range(num_of_player):
        while True:
            player_name = input(f"Enter your name[{i + 1}]: ").strip()

            if player_name == "skip":
                print("Cannot use the name 'skip'.")

            elif player_name == "":
                print("Cannot use empty names.")

            else:
                player_list.append(player_name)
                log.start.name_of_player(player_name, i)

    current_player = player_list[:]

    villager = player_list[:]


# playerにroleを指定
def assign_role():
    global wolf, maniac, villager, current_player, current_villager, current_wolf, dis_current_villager, dis_current_wolf

    # 人狼(limit)
    while True:
        try:
            wolf_limit = int(
                input(
                    f"Enter the limit number of wolf(Min 1, Max {limit.maximum_wolf(num_of_player)})"
                )
            )

            if wolf_limit >= 1 and wolf_limit <= limit.maximum_wolf(num_of_player):
                log.start.role_limit(wolf_limit, "wolf")
                break

            else:
                print(f"Minimum is 0, Maximum is {limit.maximum_wolf(num_of_player)}")

        except ValueError:
            print("Invalid input")

    # 預言者(limit)
    while True:
        try:
            seer_limit = int(
                input(
                    f"Enter the limit number of seer(Min 0, Max {limit.maximum_seer(num_of_player)}): "
                )
            )

            if seer_limit >= 0 and seer_limit <= limit.maximum_seer(num_of_player):
                log.start.role_limit(seer_limit, "seer")
                break

            else:
                print(f"Minimum is 0, maximum is {limit.maximum_seer(num_of_player)}")

        except ValueError:
            print("Invalid input")

    # 狂人(limit)
    while True:
        try:
            maniac_limit = int(
                input(
                    f"Enter the limit number of maniac(Min 0, Max {limit.maximum_maniac(num_of_player)}): "
                )
            )

            if maniac_limit >= 0 and maniac_limit <= limit.maximum_maniac(
                num_of_player
            ):
                log.start.role_limit(maniac_limit, "maniac")
                break

            else:
                print(f"Minimum is 0, Maximum is {limit.maximum_maniac(num_of_player)}")
        except ValueError:
            print("Invalid input")

    # 人狼(set)
    wolf_set = player_list[:]

    for _ in range(wolf_limit):
        idx_wolf = random.randint(0, len(wolf_set) - 1)
        wolf.append(wolf_set[idx_wolf])
        log.start.role_set("wolf", wolf_set[idx_wolf])

        villager.remove(wolf_set[idx_wolf])
        wolf_set.remove(wolf_set[idx_wolf])

    # 預言者(set)
    seer_set = wolf_set[:]

    if seer_limit >= 1:
        for _ in range(seer_limit):
            idx_seer = random.randint(0, len(seer_set) - 1)
            seer.append(seer_set[idx_seer])
            log.start.role_set("seer", seer_set[idx_seer])

            villager.remove(seer_set[idx_seer])
            seer_set.remove(seer_set[idx_seer])

    # 狂人(set)
    maniac_set = seer_set[:]

    if maniac_limit >= 1:
        for _ in range(maniac_limit):
            idx_maniac = random.randint(0, len(maniac_set) - 1)
            maniac.append(maniac_set[idx_maniac])
            log.start.role_set("maniac", maniac_set[idx_maniac])

            villager.remove(maniac_set[idx_maniac])
            maniac_set.remove(maniac_set[idx_maniac])

    # 配列に適用
    current_wolf = wolf[:]
    dis_current_wolf = wolf[:]

    for i in maniac:
        current_wolf.append(i)

    current_villager = villager[:]
    for i in seer:
        current_villager.append(i)

    dis_current_villager = current_villager[:]

    for i in maniac:
        dis_current_villager.append(i)


def player_role_dict():
    global role_dict

    for idx, player in enumerate(player_list, start=1):
        role = (
            "wolf"
            if player in wolf
            else (
                "seer"
                if player in seer
                else "maniac" if player in maniac else "villager"
            )
        )

        role_dict[idx] = {"name": player, "role": role}
