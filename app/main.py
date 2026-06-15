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
    if redirect_file :
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
    redirect_file = None
    operator = None
    if '>' in args: operator='>'
    elif '1>' in args: operator='1>'
    elif '2>' in args: operator='2>'

    if not operator:
        return args,None,None

    redirect_idx = args.index(operator)

    if redirect_idx == len(args)-1:
        print("syntax error")
        return args[redirect_idx+1], None,None

    redirect_file = args[redirect_idx +1 ]
    cleaned_args = args[:redirect_idx]
    
    stream_type = "stderr" if operator == "2>" else "stdout"    

    return cleaned_args,stream_type, redirect_file


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
        cleaned_args,stream_type,redirect_file = parse_redirect(args)

        cmd = cleaned_args[0]

        if cmd == "exit":
            break
        
        if cmd == "echo":
            target_file = redirect_file if stream_type == "stdout" else None  
            write_output(" ".join(cleaned_args), target_file)
                
        # elif cmd == "type":
        #     handle_type_cmd(args, redirect_file, is_redirect)

        else:
            try:
                if redirect_file:
                    with open(redirect_file,'w') as f:
                        if stream_type == "stderr":
                            subprocess.run(cleaned_args, stderr=f)
                        else:
                            subprocess.run(cleaned_args, stdout=f)
                else:
                    subprocess.run(cleaned_args)
            except FileNotFoundError:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
