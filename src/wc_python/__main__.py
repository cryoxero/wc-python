from argparse import ArgumentParser

def main():
    parser = ArgumentParser("wc-python", description="A version of GNU/linux wc tool, written in python by CryoXero")
    args = parser.parse_args()
    quit(0)

if __name__ == "__main__":
    main()
