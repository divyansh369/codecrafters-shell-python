import shlex
import sys
import shutil

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
            path = shutil.which(args[1])
            if args[1] in BUILTIN:
                print(f"{args[1]} is a shell builtin")
            elif path is not None:
                print(f"{args[1]} is in {path}")
            else: 
                print(f"{args[1]}: not found")
        else:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
