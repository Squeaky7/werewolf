import random
import tkinter as tk
# import json
import statistics
import os

terminal_width = os.get_terminal_size().columns

player_list = []
wolf = []
seer = []
villager = []
can_see_list = []
killed_list = []
kill_possible = []
current_player = []
vote = []
num_of_player = int()

def echooff():
    os.system("clear")

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

# # tkinter(仮)出力
# def player_input(inputText):
#     print(inputText)

# # tkinter(仮)メイン
# # def run_control(player_name, role):
#     root = tk.Tk()
#     root.title(f"{player_name}'s Control")
#     root.geometry("400x300")

#     global role_label
#     role_label = tk.Label(root, text=f"Your role is : {role}")
#     role_label.pack(pady=5)

#     global select_label
#     select_label = tk.Label(root, text="sample")
#     select_label.pack(pady=5, padx=3)

#     input_text = tk.Entry(root, width= 40)
#     input_text.pack(pady=5)

#     def on_button_click():
#         user_input = input_text.get()
#         input_text.delete(0, tk.END)
#         player_input(user_input)

#     button = tk.Button(root, text="Send", command=on_button_click)
#     button.pack(pady=10)

#     root.mainloop()
    
# # log表示
# def log_window():
#     root = tk.Tk()
#     root.title("Log")
#     root.geometry("500x350")

#     # Canvasを使ったスクロール可能なエリアの作成
#     canvas = tk.Canvas(root)
#     scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
#     scrollable_frame = tk.Frame(canvas)

#     # スクロールバーの動作をキャンバスにバインド
#     scrollable_frame.bind(
#         "<Configure>",
#         lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#     )

#     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#     canvas.configure(yscrollcommand=scrollbar.set)

#     # レイアウト配置
#     canvas.pack(side="left", fill="both", expand=True)
#     scrollbar.pack(side="right", fill="y")

#     # ログ内容の表示
#     log_lines = ["Initializing logs..."]  # 初期ログ

#     def update_logs():
#         new_line = f"New log entry {len(log_lines)}"  # 新しいログを作成
#         log_lines.append(new_line)  # ログに追加
#         for widget in scrollable_frame.winfo_children():
#             widget.destroy()  # 古いラベルを削除

#         # 全てのログを表示
#         for line in log_lines:
#             tk.Label(scrollable_frame, text=line, anchor="w", justify="left").pack(fill="x")

#         # スクロール位置を最下部に移動
#         canvas.yview_moveto(1.0)

#         # 一定時間後に再度呼び出し
#         root.after(1000, update_logs)

#     update_logs()  # ログの更新開始

#     root.mainloop()

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
        limit_wolf = int(input(f"Enter the number of wolf(Min 1, Max {maximum_wolf(num_of_player)}): "))
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

# playerとroleをdict形式に保存
def dict_player_roles():
    global player_role
    player_role = {}
    for index, player in enumerate(player_list, start=1):
        role = (
            "wolf" if player in wolf
            else "seer" if player in seer
            else "villager"
        )
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
            kill = int(input(f"Select the player you want to kill: "))
            killed_list.append(kill_possible[kill - 1])
            print(f"Killed {kill_possible[kill - 1]}")
            # current_player.remove(kill_possible[kill - 1])
            kill_possible.remove(kill_possible[kill - 1])
            break
        except:
            print("Invalid input")
    

def wolf_move():
    print("You are a wolf.")
    wolf_option()


def seer_move(player):
    print("You are a seer.")
    can_see_list.remove(player)

    if not player in killed_list:
        for i in range(len(can_see_list)):
            print(f"{i + 1}. {can_see_list[i]}")

        print("Select players and confirm roles: ")
        while True:
            try:
                see_player = int(input())
                if can_see_list[see_player - 1] in wolf:
                    print(f"{can_see_list[see_player - 1]} is BLACK!")
                else:
                    print(f"{can_see_list[see_player - 1]} is WHITE!")
                break
            except:
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
        global current_player, can_see_list
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
                wolf_move()

        for player in killed_list:
            current_player.remove(player)

        can_see_list = current_player[:]

        input()

    # 昼サイクル
    def day_cycle():
        global killed_list, current_player, wolf
        for i in killed_list:
            print(f"{i} was killed.")
        
        killed_list = []
        print("-" * terminal_width)
        print("The devate time is 2 minutes.\nAfter the end the debate, it is time to vote.")
        print("List of remaining players: ", end="")
        for name in current_player:
            print(f"{name}, ", end="")
        print()
        input()  

        # vote[投票]
        echooff()
        for _ in current_player:
            echooff()
            print(f"Select a player you want vote['skip' to skip]: ")
            for list in range(len(current_player)):
                print(f"{list + 1}. {current_player[list]}")

            while True:
                select_vote = input()
                try:
                    print(f"You voted in {current_player[int(select_vote) - 1]}")
                    vote.append(current_player[int(select_vote) - 1])
                    break
                except:
                    if select_vote == "skip":
                        vote.append("skip")
                        break
                    else:
                        print("Invalid input.")

        echooff()

        # 開票
        if statistics.multimode(vote) == ['skip']:
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
            print(f"{len(wolf)} werewolves remain.")
        
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

