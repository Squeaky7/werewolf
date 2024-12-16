import random

# import json
import statistics
import os
import display_log as log
import role_limit as limit

terminal_width = os.get_terminal_size().columns

# _____________________________________________________________________________________________________________________
# list宣言

# プレイヤーを保存
player_list = []

# role別に保存
wolf = []  # 人狼
seer = []  # 預言者
villager = []  # 市民
maniac = []  # 狂人

# 生存人数
current_wolf = []
current_villager = []


# role別の動作用
can_see_list = []  # 預言可能リスト(預言者)
killed_list = []  # 殺されたリスト(人狼)
kill_possible = []  # 殺せるリスト(人狼)
current_player = []  # 現在生きてるリスト
vote = []  # 投票箱

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# ゲーム進行で使うもの(list以外)

# player人数
num_of_player = int()

# 詳細情報表示
timeslot = "Role Check"  # 時間帯表示(昼/夜)
remplayer = {}


# player情報 [ Wolf : x , Villager : y , Total : z]
def rem():
    remplayer = {
        "Wolf": len(current_wolf),
        "Villager": len(current_villager),
        "Total": len(current_player),
    }

    return remplayer


# listをstrに変換
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


# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


# ゲーム初期設定
# ________________________________________________________________________________________________________________________


# プレイヤー数、名前を取得
def get_player_names():
    global player_list, num_of_player, villager

    while True:
        try:
            num_of_player = int(input("Enter the number of players: "))
            if num_of_player >= 3:
                log.start.number_of_player(num_of_player)
                break

            else:
                print("This game can't be played with less than 3 people.")

        except ValueError:
            print("Please enter a valid number.")

    if num_of_player < 3:
        print("This game can't be played with less than 3 people.")

    # プレイヤーの名前を取得
    for i in range(num_of_player):
        while True:
            user_name = input(f"Enter your name[{i+1}]: ").strip()
            if not user_name == "skip":
                player_list.append(user_name)
                log.start.name_of_player(user_name, i)
                break
            else:
                print("The name can't use.")

    villager = player_list[:]
    # print(player_list)


# プレイヤーにロールを指定
def assign_roles():
    global wolf, seer, villager, current_wolf, current_villager, current_player

    # 人狼
    while True:
        try:
            limit_wolf = int(
                input(
                    f"Enter the number of wolf(Min 1, Max {limit.maximum_wolf(num_of_player)}): "
                )
            )

            if limit_wolf >= 1 and limit_wolf <= limit.maximum_wolf(num_of_player):
                log.start.role_limit(limit_wolf, "wolf")
                break

            else:
                print(f"Minimum is 1, maximum is {limit.maximum_wolf(num_of_player)}")

        except ValueError:
            print("Invalid input")

    wolf_set = player_list[:]

    for _ in range(limit_wolf):
        set_wolf = random.randint(0, len(wolf_set) - 1)
        log.start.role_set("wolf", wolf_set[set_wolf])
        wolf.append(wolf_set[set_wolf])
        villager.remove(wolf_set[set_wolf])
        del wolf_set[set_wolf]

    # print(wolf, wolf_set, player_list)

    # 預言者
    if num_of_player > 4:
        seer_set = wolf_set[:]

        while True:
            limit_seer = int(
                input(
                    f"Enter the number of seer(Min 0, Max {limit.maximum_seer(num_of_player)}): "
                )
            )

            if limit_seer >= 0 and limit_seer <= limit.maximum_seer(num_of_player):
                log.start.role_limit(limit_seer, "seer")
                break

            else:
                print(f"Minimum is 0, maximum is {limit.maximum_seer(num_of_player)}")

        if limit_seer > 0:

            for _ in range(limit_seer):
                set_seer = random.randint(0, len(seer_set) - 1)
                log.start.role_set("seer", seer_set[set_seer])
                seer.append(seer_set[set_seer])
                villager.remove(seer_set[set_seer])
                del seer_set[set_seer]

    # 狂人
    if num_of_player > 4:
        maniac_set = seer_set[:]

        while True:
            limit_maniac = int(
                input(
                    f"Enter the number of maniac(Min 0, Max {limit.maximum_maniac(num_of_player)}: )"
                )
            )

            if limit_maniac >= 0 and limit_maniac <= limit.maximum_maniac(
                num_of_player
            ):
                log.start.role_limit(limit_maniac, "maniac")
                break

            else:
                print(f"Minimum is 0, maximum is {limit.maximum_maniac(num_of_player)}")

        if limit_maniac > 0:

            for _ in range(limit_maniac):
                set_maniac = random.randint(0, len(maniac_set) - 1)
                log.start.role_set("maniac", maniac_set[set_maniac])
                maniac.append(maniac_set[set_maniac])
                villager.remove(maniac_set[set_maniac])
                del maniac_set[set_maniac]

    current_wolf = wolf[:]
    current_villager = villager[:]

    for i in maniac:
        current_villager.append(i)

    for i in seer:
        current_villager.append(i)


# playerとroleをdict形式に保存
def dict_player_roles():
    global player_role
    player_role = {}

    for index, player in enumerate(player_list, start=1):
        role = "wolf" if player in wolf else "seer" if player in seer else "villager"
        player_role[index] = {"name": player, "role": role}

    # print(json.dumps(player_role, indent= 4))


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


# 人狼サイクル
# ________________________________________________________________________________________________________________________


def role_check():
    for i in current_player:
        echooff()

        print(f"Change to {i}")
        input()
        echooff()

        print(f"{i}'s turn")
        input()

        print("Your role is ", end="")

        if i in villager:

            print("villager.")
        elif i in seer:

            print_color("seer.", "blue")
            print()
        elif i in wolf:

            print_color("wolf.")
            print_color("\nWolf team is ")
            for i in wolf:
                print_color(f"{i}, ")
            print()

        elif i in maniac:
            print_color("maniac.", "red")
            print("\nWolf is ", end="")

            for werewolf in wolf:
                print_color(f"{werewolf} ")
            print(".")

        input("Press enter when finish check ▶︎")


def wolf_option(name):
    global killed_list, kill_possible

    for i in range(len(kill_possible)):
        print(f"{i + 1}. {kill_possible[i]}")

    while True:
        try:
            kill = int(input("Select the player you want to kill: "))
            killed_list.append(kill_possible[kill - 1])
            print_color(f"Killed {kill_possible[kill - 1]}", "yellow")
            log.cycle.killed(name, kill_possible[kill - 1], "wolf")
            print()
            # current_player.remove(kill_possible[kill - 1])

            kill_possible.remove(kill_possible[kill - 1])
            break

        except IndexError:
            print("Index error")

        except ValueError:
            print("Invalid input")


def wolf_move(name):
    print("You role is wolf.")
    wolf_option(name)


def seer_move(player):
    print("You are a seer.")
    can_see_list.remove(player)

    if player not in killed_list:

        for i in range(len(can_see_list)):
            print(f"{i + 1}. {can_see_list[i]}")

        print("Select players and confirm roles: ", end="")

        while True:
            try:
                see_player = int(input())

                if can_see_list[see_player - 1] in wolf:
                    print_color(f"{can_see_list[see_player - 1]} is BLACK!", "red")
                    print()

                else:
                    print_color(f"{can_see_list[see_player - 1]} is WHITE!", "green")
                    print()

                break

            except ValueError:
                print("Invalid input")


def villager_move():
    print("You are a villager. You have no movement.")


def maniac_move():
    print("You are a maniac. You have no movement.")


def move_cycle():
    global can_see_list, kill_possible, current_player, killed_list, wolf, current_wolf, current_villager
    kill_possible = villager[:]

    for i in seer:
        kill_possible.append(i)

    for i in maniac:
        kill_possible.append(i)

    current_player = player_list[:]

    # 夜サイクル
    def night_cycle():
        global current_player, can_see_list, timeslot
        timeslot = "Night Time"
        can_see_list = current_player[:]

        for player in current_player:
            print(f"Change to {player}(Press Enter to continue)")
            input()
            echooff()

            print(f"{player}'s turn[Enter]")
            input()

            if player in villager:
                villager_move()

            elif player in seer:
                seer_move(player)

            elif player in wolf:
                wolf_move(player)

            elif player in maniac:
                maniac_move()

        for player in killed_list:
            current_player.remove(player)

        input()

    # 昼サイクル
    def day_cycle():
        global killed_list, current_player, wolf, timeslot, current_villager, current_wolf, kill_possible
        timeslot = "Day Time"

        for i in killed_list:
            current_villager.remove(i)
            print_color(f"{i} was killed.")
            print()

        killed_list = []
        print("-" * terminal_width)

        print(
            "The devate time is 2 minutes.\nAfter the end the debate, it is time to vote."
        )

        print("List of remaining players: ", end="")

        for name in current_player:
            print(f"{name}, ", end="")

        print()
        input()

        # vote[投票]
        echooff()
        for i in current_player:
            echooff()
            print(f"{i}'s vote\n\nSelect a player you want vote['skip' to skip]: ")

            for list in range(len(current_player)):
                print(f"{list + 1}. {current_player[list]}")

            while True:
                select_vote = input()
                try:
                    print(f"You voted in {current_player[int(select_vote) - 1]}")
                    vote.append(current_player[int(select_vote) - 1])
                    break

                except IndexError:
                    print(f"Enter an integer between 1 and {len(current_player)}")

                except ValueError:
                    if select_vote == "skip":
                        vote.append("skip")
                        break

                    else:
                        print("Invalid input.")

        echooff()

        # 開票
        if statistics.multimode(vote) == ["skip"]:
            print("This vote is skipped.")

        elif len(statistics.multimode(vote)) > 1:
            print("As the number of votes was the same, no vote was taken.")

        else:
            print_color(f"{tally(statistics.multimode(vote))} was exiled.\n", "yellow")
            log.cycle.exile(tally(statistics.multimode(vote)))

            for i in statistics.multimode(vote):
                current_player.remove(i)

                if i in wolf:
                    print_color(f"{i} was a werewolf.\n", "green")
                    print()
                    current_wolf.remove(i)
                    wolf.remove(i)

                else:
                    print_color(f"{i} was not a werewolf.\n")
                    current_villager.remove(i)
                    kill_possible.remove(i)

    # ゲーム終了処理
    def game_condition():
        if len(wolf) * 2 >= len(current_player):
            return "wolf"
        elif len(wolf) == 0:
            return "villager"
        else:
            return None

    role_check()

    # 繰り返し処理
    while True:
        night_cycle()
        echooff()

        if game_condition() == "wolf":
            for i in killed_list:
                print_color(f"{i} was killed.")
                print()

            print_color("Wolf team wins!\n")
            log.cycle.end_game("wolf")
            log.start.return_log()
            break

        elif game_condition() == "villager":
            print_color("Villager team wins!", "green")
            log.cycle.end_game("villager")
            log.start.return_log()
            break

        elif len(wolf) == 1:
            print(f"{len(wolf)} werewolf remain.")

        else:
            print(f"{len(wolf)} werewolfs remain.")

        day_cycle()

        if game_condition() == "wolf":
            print("Wolf team wins!")
            log.cycle.end_game("wolf")
            log.start.return_log()
            break

        elif game_condition() == "villager":
            print("Villager team wins!")
            log.cycle.end_game("villager")
            log.start.return_log()
            break

        elif len(wolf) == 1:
            print(f"{len(wolf)} werewolf remain.")

        else:
            print(f"{len(wolf)} werewolfs remain.")


# mainメソッド
def main():
    get_player_names()
    assign_roles()
    dict_player_roles()
    echooff()
    move_cycle()


if __name__ == "__main__":
    main()
