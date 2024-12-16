# ロール確認
# 夜の動き
# 昼の動き
# 投票
# 人狼に噛まれた時
# 占われた時

import os
import werewolf


# _____________________________________________________________________________________________________________________
# 初期設定

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
    print(werewolf.o_detail(werewolf.timeslot, werewolf.rem()))


# 初期設定
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


class GameSetUp:
    def role_check():
        echooff()
        print("Your role is ")
        print_color("Villager", "green")
        input()


class GameAction:
    def night_action():
        echooff()
        print("You are a villager. You have no movement.")
        input()

    def day_action():
        print("Discuss")

    def vote_action(player_name):
        echooff()
        print(f"{player_name}'s vote")
        input()

        print("Select a player you want to vote['skip' to skip]: ")

        for pl_num, candidate in enumerate(werewolf.current_player):
            print(f"{pl_num + 1}. {candidate}")

        while True:
            selected_vote = input()

            try:
                print(f"You voted in {werewolf.current_player[int(selected_vote)]}")
                werewolf.vote.append(werewolf.current_player[int(selected_vote - 1)])
                break

            except IndexError:
                print(f"Enter an integer between 1 and {len(werewolf.current_player)}")

            except ValueError:
                if selected_vote == "skip":
                    werewolf.vote.append("skip")
                    break

                else:
                    print("Invalid input.")

        echooff()

    def bite_by_wolf(player_name):
        werewolf.killed_list.append(player_name)
        werewolf.kill_possible.remove(player_name)

    def predicted_by_seer(player_name):
        echooff()
        print_color(f"{player_name} is WHITE", "green")
        input()
