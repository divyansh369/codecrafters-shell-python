import shlex
import sys
import shutil
import subprocess

BUILTIN = {"echo", "type", "exit"}

def write_output(text, redirect_file=None):
    if redirect_file:
        with open(redirect_file,'w') as f:
            f.write(text+'\n')
    else:
        print(text)

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

        is_redirect = False
        redirect_file = None

        if '>' in args or '1>' in args:
            is_redirect = True
            redirect_idx = args.index('1>') if '1>' in args else args.index('>')
            if redirect_idx == len(args) -1:
                print("syntax error")
                continue
            redirect_file = args[redirect_idx+1]
            args = args[:redirect_idx]

        cmd = args[0]

        if cmd == "exit":
            break
        
        if cmd == "echo":
            write_output(" ".join(args[1:]), redirect_file)

        elif cmd == "type":
            if len(args) < 2:
                print("type: missing operand")
                continue
            target = args[1]
            path = shutil.which(target)
            if target in BUILTIN:
                write_output(f"{target} is a shell builtin")
            elif path is not None:
                if is_redirect:
                    write_output(f"{target} is {path}", redirect_file)
                else:
                    write_output(f"{target} is {path}")
            else:
                write_output(f"{target}: not found", redirect_file)
        else:
            try:
                if redirect_file:
                    with open(redirect_file,'w') as f:
                        subprocess.run(args, stdout=f)
                else:
                    subprocess.run(args)
            except FileNotFoundError:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()