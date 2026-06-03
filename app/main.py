import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        if command.startswith("echo "):
            print(command[5:])
        elif command.startswith("type "):
            cmd = command[5:]
            if cmd in ["echo", "type","exit"]:
                print(f"{command[5:]} is a shell builtin")
            else:
                print(f"{command[5:]}: not found")
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
