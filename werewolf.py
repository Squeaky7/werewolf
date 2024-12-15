import random

# import json
import statistics
import os

terminal_width = os.get_terminal_size().columns

# _____________________________________________________________________________________________________________________
# list宣言

# プレイヤーを保存
player_list = []

# role別に保存
wolf = []  # 人狼
seer = []  # 預言者
villager = []  # 市民
maniac = []


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
timeslot = "Night Time"  # 時間帯表示(昼/夜)
remplayer = {}


# player情報
def rem():
    remplayer = {
        "Wolf": len(wolf),
        "Villager": len(villager) + len(seer),
        "Total": len(player_list),
    }
    return remplayer


# コマンドクリア
def echooff():
    os.system("clear")
    print(o_detail(timeslot, rem()))


# 詳細を返す
def o_detail(timeslot, rem1):
    detail = f"[ {timeslot} ] [ Wolf : {rem1["Wolf"]} , Villager : {rem1["Villager"]} , Total : {rem1["Total"]}]"
    return detail


# ゲーム初期設定
# ________________________________________________________________________________________________________________________
# 人狼の人数上限
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


# 預言者の人数上限
def maximum_seer(number_of_player):
    if number_of_player <= 6:
        return 1
    elif number_of_player <= 11:
        return 2


# プレイヤー数、名前を取得
def get_player_names():
    global player_list, num_of_player, villager
    player_list = []
    while True:
        try:
            num_of_player = int(input("Enter the number of players: "))
            if num_of_player >= 3:
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
                break
            else:
                print("The name can't use.")

    villager = player_list[:]
    # print(player_list)


# プレイヤーにロールを指定
def assign_roles():
    global wolf, seer, villager
    # 人狼
    while True:
        limit_wolf = int(
            input(
                f"Enter the number of wolf(Min 1, Max {maximum_wolf(num_of_player)}): "
            )
        )
        if limit_wolf >= 1 and limit_wolf <= maximum_wolf(num_of_player):
            break
        else:
            print(f"Minimum is 1, maximum is {maximum_wolf(num_of_player)}")

    wolf_set = player_list[:]
    for _ in range(limit_wolf):
        set_wolf = random.randint(0, len(wolf_set) - 1)
        wolf.append(wolf_set[set_wolf])
        villager.remove(wolf_set[set_wolf])
        del wolf_set[set_wolf]

    # print(wolf, wolf_set, player_list)

    # 預言者
    if num_of_player > 4:
        seer_set = wolf_set[:]
        while True:
            limit_seer = int(input(f"Enter the number of seer(Min 0, Max {3}): "))
            if limit_seer >= 0 and limit_seer <= 3:
                break
            else:
                print(f"Minimum is 0, maximum is {3}")

        if limit_seer > 0:
            for _ in range(limit_seer):
                set_seer = random.randint(0, len(seer_set) - 1)
                seer.append(seer_set[set_seer])
                villager.remove(seer_set[set_seer])
                del seer_set[set_seer]

    if num_of_player > 4:
        maniac_set = seer_set[:]
        while True:
            limit_maniac = int(input(f"Enter the number of maniac(Min 0, Max {3})"))
            if limit_maniac >= 0 and limit_maniac <= 3:
                break
            else:
                print(f"Minimum is 0, maximum is {3}")

        if limit_maniac > 0:
            for _ in range(limit_maniac):
                set_maniac = random.randint(0, len(maniac_set) - 1)
                maniac.append(maniac_set[set_maniac])
                villager.remove(maniac_set[set_maniac])
                del maniac_set[set_maniac]


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


def wolf_option():
    for i in range(len(kill_possible)):
        print(f"{i + 1}. {kill_possible[i]}")

    while True:
        try:
            kill = int(input("Select the player you want to kill: "))
            killed_list.append(kill_possible[kill - 1])
            print(f"Killed {kill_possible[kill - 1]}")
            # current_player.remove(kill_possible[kill - 1])
            kill_possible.remove(kill_possible[kill - 1])
            break
        except ValueError:
            print("Invalid input")


def wolf_move():
    print("You role is wolf.")
    wolf_option()


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
                    print(f"{can_see_list[see_player - 1]} is BLACK!")
                else:
                    print(f"{can_see_list[see_player - 1]} is WHITE!")
                break
            except ValueError:
                print("Invalid input")


def villager_move():
    print("You are a villager. You have no movement.")


def move_cycle():
    global can_see_list, kill_possible, current_player, killed_list, wolf
    can_see_list = player_list[:]
    kill_possible = villager[:]
    for i in seer:
        kill_possible.append(i)
    current_player = player_list[:]

    # 夜サイクル
    def night_cycle():
        global current_player, can_see_list, timeslot
        timeslot = "Nigt Time"
        for player in current_player:
            print(f"Change to {player}(Press Enter to continue)")
            input()
            echooff()
            print(f"{player}'s turn[Enter]")
            input()
            print()
            if player in villager:
                villager_move()
            elif player in seer:
                seer_move(player)
            elif player in wolf:
                wolf_move()

        for player in killed_list:
            current_player.remove(player)

        can_see_list = current_player[:]

        input()

    # 昼サイクル
    def day_cycle():
        global killed_list, current_player, wolf, timeslot
        timeslot = "Day Time"
        for i in killed_list:
            print(f"{i} was killed.")

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
            print(f"{i}'s vote\nSelect a player you want vote['skip' to skip]: ")
            for list in range(len(current_player)):
                print(f"{list + 1}. {current_player[list]}")

            while True:
                select_vote = input()
                try:
                    print(f"You voted in {current_player[int(select_vote) - 1]}")
                    vote.append(current_player[int(select_vote) - 1])
                    break
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
            print(f"{statistics.multimode(vote)} was expelled.")
            for i in statistics.multimode(vote):
                current_player.remove(i)
                if i in wolf:
                    print(f"{i} was a werewolf.")
                    wolf.remove(i)
                else:
                    print(f"{i} was not a werewolf.")

    # ゲーム終了処理
    def game_condition():
        if len(wolf) * 2 >= len(current_player):
            return "wolf"
        elif len(wolf) == 0:
            return "villager"
        else:
            return None

    # 繰り返し処理
    while True:
        night_cycle()
        echooff()

        if game_condition() == "wolf":
            print("Wolf team wins!")
            break
        elif game_condition() == "villager":
            print("Villager team wins!")
            break
        else:
            print(f"{len(wolf)} werewolfs remain.")

        day_cycle()

        if game_condition() == "wolf":
            print("Wolf team wins!")
            break
        elif game_condition() == "villager":
            print("Villager team wins!")
            break
        else:
            print(f"{len(wolf)} werewolves remain.")


# mainメソッド
def main():
    get_player_names()
    assign_roles()
    dict_player_roles()
    echooff()
    move_cycle()


if __name__ == "__main__":
    main()
