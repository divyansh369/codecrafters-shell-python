import shlex
import sys
import shutil
import subprocess

BUILTIN = {"echo", "type", "exit"}

def write_output(text, redirect_file=None):
    '''
        Outputs text to either a file or terminal, automatically handling newlines.
        Args:
            Text: The text to be written to the output.
        redirect_file (str | None): The file to which the output should be redirected. If None, the output

    '''
    if redirect_file:
        with open(redirect_file,'w') as f:
            f.write(text+'\n')
    else:
        print(text)

def parse_redirect(args):
    '''
        Parses the command arguments to check for output redirection and identifies the target file if redirection is present.
        Args:
            args (list): The list of command arguments to be parsed for redirection.
        Returns:
            tuple: A tuple containing a boolean indicating whether redirection is present and the target file for
    '''
    is_redirect = False
    redirect_file = None

    if '>' in args or '1>' in args:
        is_redirect = True
        redirect_idx = args.index('1>') if '1>' in args else args.index('>')
        if redirect_idx == len(args) -1:
            print("syntax error")
            return is_redirect, redirect_file
        redirect_file = args[redirect_idx+1]
        args = args[:redirect_idx]
    
    return is_redirect, redirect_file

def handle_type_cmd(args,redirect_file,is_redirect):
    '''
        Handles the 'type' command by determining if the specified command is a shell builtin, an executable in the system's PATH, or not found.
        Args:
            args (list): The list of command arguments, where the second element is the target command to be checked.
            redirect_file (str | None): The file to which the output should be redirected. If None, the output will be printed to the terminal.
            is_redirect (bool): A boolean indicating whether output redirection is present.
    '''
    if len(args) < 2:
        print("type: missing operand")
        return 
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
        is_redirect, redirect_file = parse_redirect(args)

        cmd = args[0]

        if cmd == "exit":
            break
        
        if cmd == "echo":
            write_output(" ".join(args[1:]), redirect_file)

        elif cmd == "type":
            handle_type_cmd(args, redirect_file, is_redirect)

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
