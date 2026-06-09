import shlex
import sys
import shutil
import subprocess

BUILTIN = {"echo", "type", "exit"}

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        
        if not user_input:
            continue
        
        args = shlex.split(user_input)
        cmd = args[0]

        if cmd == "exit":
            break

        if cmd == "echo":
            print(" ".join(args[1:]))
        
        elif cmd == "type":
            if len(args) < 2:
                print("type: missing operand")
                continue
            target = args[1]
            path = shutil.which(target)
            if target in BUILTIN:
                print(f"{target} is a shell builtin")
            elif path is not None:
                print(f"{target} is {path}")
            else:
                print(f"{target}: not found")
        else:
            try:
                subprocess.run(args)
            except FileNotFoundError:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
