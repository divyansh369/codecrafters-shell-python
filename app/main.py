import sys


def main():
    sys.stdout.write("$ ")
    command = input()
    if command:
        print(f"{command}: command not found\n")

if __name__ == "__main__":
    main()