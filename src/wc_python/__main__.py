from argparse import ArgumentParser
from os.path import exists, isdir, getsize
from sys import stdin

def get_file_details(path):
    details = {
        "error": False,
        "exists": True,
        "is_file": True,
        "bytes": 0
    }
    if not exists(path):
        details["exists"] = False
        return details
    if isdir(path):
        details["is_file"] = False
        return details
    
    try:
        # BYTES
        details["bytes"] = getsize(path)
    except Exception:
        details["error"] = True
    
    return details


def get_stdin_details():
    details = {
        "error": False,
        "bytes": 0,
    }

    try:
        for char in stdin.read():
            # BYTES
            details["bytes"] += len(char.encode("utf-8"))
    except Exception:
        details["error"] = True

    return details


def main():
    parser = ArgumentParser("wc-python", description="A version of GNU/linux wc tool, written in python by CryoXero")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    args = parser.parse_args()
    quit(0)

if __name__ == "__main__":
    #main()
    print(get_stdin_details())
