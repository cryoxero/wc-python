from argparse import ArgumentParser
from os.path import exists, isdir, getsize
from sys import stdin

def get_file_details(path):
    details = {
        "error": False,
        "exists": True,
        "is_file": True,
        "bytes": 0,
        "chars": 0,
        "lines": 0,
        "words": 0,
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
                # LINES
                details["lines"] += 1
                for char in line:
                    # CHARS
                    details["chars"] += 1
                    # WORDS
                    if char.isspace():
                        if is_word:
                            details["words"] += 1
                        is_word = False
                    else:
                        is_word = True
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
    }

    try:
        is_word = False
        for char in stdin.read():
            if char.isspace():
                # LINES
                if is_word:
                    details["words"] += 1
                if char == "\n":
                    details["lines"] += 1
                is_word = False
            else:
                is_word = True

            # BYTES
            details["bytes"] += len(char.encode("utf-8"))
            # CHARS
            details["chars"] += 1
        # LAST WORD CHECK
        if is_word:
            details["words"] += 1
    
    except Exception:
        details["error"] = True

    return details


def main():
    parser = ArgumentParser("wc-python", description="A version of GNU/linux wc tool, written in python by CryoXero")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    args = parser.parse_args()
    quit(0)

if __name__ == "__main__":
    main()
