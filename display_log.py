from datetime import datetime
import os

log = []
log_number = 0

log.append(f"[{datetime.now()}] Started game...")

logs_path = "logs"


class start:
    global log_number, log

    def return_log():
        for i in log:
            print(i)

    def number_of_player(num_of_player):
        global log_number, log
        log.append(f"[{datetime.now()}] Set the number of players to {num_of_player}")
        log_number = +1

    def name_of_player(name, player_number):
        global log_number, log
        log.append(
            f'[{datetime.now()}] Set the player({player_number + 1})\'s name to "{name}"'
        )
        log_number = +1

    def role_limit(limit, role):
        global log_number, log
        log.append(f"[{datetime.now()}] Set the number of {role} to {limit}")
        log_number = +1

    def role_set(role, name):
        global log_number, log
        log.append(f'[{datetime.now()}] Set the role of "{name}" to {role}')
        log_number = +1


class cycle:
    global log_number, log

    def killed(wolf, murdered, role):
        global log_number, log
        log.append(f'[{datetime.now()}] "{murdered}" killed by {role} "{wolf}"')
        log_number = +1

    def exile(name):
        global log_number, log
        log.append(f'[{datetime.now()}] "{name}" was exiled')
        log_number = +1

    def end_game(won_side):
        global log_number, log

        now = datetime.now()

        if won_side == "wolf":
            log.append(f"[{now}] Wolf team wins")
        elif won_side == "villager":
            log.append(f"[{now}] Villager team wins")
        log.append(f"[{now}] End of game")
        log_number = +1

        if not os.path.exists(logs_path):
            try:
                os.makedirs(logs_path)

            except OSError as e:
                print(f"Failed to create directory '{logs_path}': {e}")
                return

        format_date = now.strftime("%Y-%m-%d-%H-%M-%S")
        script_dir = os.path.dirname(os.path.abspath(__file__))

        logs_file_path = os.path.join(script_dir, "logs", f"{format_date}.log")

        try:
            with open(logs_file_path, "a") as f:
                for line in log:
                    f.write(line + "\n")

            print(f"Log saved to {logs_file_path}")

        except OSError as e:
            print(f"Error writing to log file '{logs_file_path}': {e}")


def main():
    for i in log:
        print(i)


if __name__ == "__main__":
    main()
