from argparse import ArgumentParser
from os.path import exists, isdir, getsize
from sys import stdin
from enum import Enum

class States(Enum):
    BYTES = 1
    CHARS = 2
    LINES = 4
    WORDS = 8
    LONGEST = 16


def get_state(args):
    state = 0
    
    state |= int(args.lines) * States.LINES.value
    state |= int(args.words) * States.WORDS.value
    state |= int(args.bytes) * States.BYTES.value
    state |= int(args.chars) * States.CHARS.value
    state |= int(args.max_line_length) * States.LONGEST.value
    
    return state or States.LINES.value | States.WORDS.value | States.BYTES.value


def get_file_details(path):
    details = {
        "error": False,
        "exists": True,
        "is_file": True,
        "bytes": 0,
        "chars": 0,
        "lines": 0,
        "words": 0,
        "longest": 0,
    }
    if not exists(path):
        details["exists"] = False
        return details
    if isdir(path):
        details["is_file"] = False
        return details
    
    try:
        is_word = False
        # BYTES
        details["bytes"] = getsize(path)
        with open(path, "r") as file:
            for line in file:
                line_length = 0
                # LINES
                details["lines"] += 1
                for char in line:
                    # CHARS
                    line_length += 1
                    # WORDS
                    if char.isspace():
                        if is_word:
                            details["words"] += 1
                        is_word = False
                    else:
                        is_word = True
                
                # LONGEST_LINE
                if line_length > details["longest"]:
                    details["longest"] = line_length - int(line[-1] == "\n")
                
                # TOTAL CHARS
                details["chars"] += line_length;
            
            # LAST WORD CHECK
            if is_word:
                details["words"] += 1

    except Exception:
        details["error"] = True
    
    return details


def get_stdin_details():
    details = {
        "error": False,
        "bytes": 0,
        "chars": 0,
        "words": 0,
        "lines": 0,
        "longest": 0,
    }

    try:
        is_word = False
        line_length = 0
        for char in stdin.read():
            if char.isspace():
                # LINES
                if is_word:
                    details["words"] += 1
                if char == "\n":
                    if line_length > details["longest"]:
                        details["longest"] = line_length - 1
                    details["lines"] += 1
                    line_length = 0
                is_word = False
            else:
                is_word = True

            # BYTES
            details["bytes"] += len(char.encode("utf-8"))
            # CHARS
            details["chars"] += 1
            line_length += 1
        # LAST WORD CHECK
        if is_word:
            details["words"] += 1

        if line_length > details["longest"]:
            details["longest"] = line_length
    except KeyboardInterrupt:
        return details
    except Exception:
        details["error"] = True

    return details


def report(state, details, path=""):
    if state & States.LINES.value:
        print(f'{details["lines"]:3}', end="\t")
    if state & States.WORDS.value:
        print(f'{details["words"]:3}', end="\t")
    if state & States.BYTES.value:
        print(f'{details["bytes"]:3}', end="\t")
    if state & States.CHARS.value:
        print(f'{details["chars"]:3}', end="\t")
    if state & States.LONGEST.value:
        print(f'{details["longest"]:3}', end="\t")
    print(path)


def main():
    parser = ArgumentParser("wc-python", description="A version of GNU/linux wc tool, written in python by CryoXero")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    parser.add_argument("-L", "--max-line-length", action="store_true", help="print the maximum display width")
    parser.add_argument("FILE", type=str, nargs="*", help="With no FILE, or when FILE is -, read standard input.")
    args = parser.parse_args()
    state = get_state(args)
    if not args.FILE:
        details = get_stdin_details()
        if details["error"]:
            quit(1)
        report(state, details)
    else:
        for path in args.FILE:
            if path == "-":
                details = get_stdin_details()
                if details["error"]:
                    quit(1)
                report(state, details)
            else:
                details = get_file_details(path)
                if not details["exists"]:
                    print(f"No such file or directory: {path}")
                    continue
                if not details["is_file"]:
                    print(f"Is a directory: {path}")
                    continue
                if details["error"]:
                    quit(1)
                report(state, details, path)
    quit(0)

if __name__ == "__main__":
    main()
