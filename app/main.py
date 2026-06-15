import shlex
import shutil
import subprocess
import sys

BUILTIN = {"echo", "type", "exit"}


def write_output(text, target_file=None):
    """Outputs text to either an appended file or terminal safely."""
    if target_file:
        with open(target_file, "a") as f:
            f.write(text + "\n")
    else:
        print(text)


def parse_redirect(args):
    """Parses command arguments to find redirection targets and stream types."""
    operator = None
    if ">" in args:
        operator = ">"
    elif "1>" in args:
        operator = "1>"
    elif "2>" in args:
        operator = "2>"

    if not operator:
        return args, None, None

    redirect_idx = args.index(operator)

    # Fixed syntax error return tracking
    if redirect_idx == len(args) - 1:
        print("syntax error: missing file after redirection operator")
        return args[:redirect_idx], None, None

    redirect_file = args[redirect_idx + 1]
    cleaned_args = args[:redirect_idx]
    stream_type = "stderr" if operator == "2>" else "stdout"

    return cleaned_args, stream_type, redirect_file


def handle_type_cmd(cleaned_args, target_file):
    """Determines if a command is a builtin or locates its path binary."""
    if len(cleaned_args) < 2:
        print("type: missing operand")
        return

    target = cleaned_args[1]
    path = shutil.which(target)

    if target in BUILTIN:
        write_output(f"{target} is a shell builtin", target_file)
    elif path is not None:
        write_output(f"{target} is {path}", target_file)
    else:
        write_output(f"{target}: not found", target_file)


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input.strip():
            continue

        # 1. Parse and validate arguments
        args = shlex.split(user_input)
        cleaned_args, stream_type, redirect_file = parse_redirect(args)

        if not cleaned_args:
            continue

        # 2. Upfront file preparation
        # Truncate/create the file once right here, satisfying file checks immediately.
        if redirect_file:
            with open(redirect_file, "w") as f:
                pass

        cmd = cleaned_args[0]
        target_file = redirect_file if stream_type == "stdout" else None

        # 3. Command Router
        if cmd == "exit":
            break

        elif cmd == "echo":
            write_output(" ".join(cleaned_args[1:]), target_file)

        elif cmd == "type":
            handle_type_cmd(cleaned_args, target_file)

        else:
            try:
                if redirect_file:
                    # Switch to 'a' (append) here since the file was already truncated above
                    with open(redirect_file, "a") as f:
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