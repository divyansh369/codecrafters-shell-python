import shlex
import sys
import shutil

def main():
    BUILTIN = ["echo", "type", "exit"]
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input()
        except EOFError or KeyboardInterrupt:
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
            if args[1] in BUILTIN:
                print(f"{args[1]} is a shell builtin")
            elif shutil.which(args[1]) is not None:
                print(f"{args[1]} is {shutil.which(args[1])}")
            else: 
                print(f"{args[1]}: not found")
        else:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()