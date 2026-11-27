import sys

if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            from src.ConfigParser import ConfigParser
            config = ConfigParser.from_file(argv[1])
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\nError: Expected exactly one configuration file."
              "\nUsage: python3 pac-man.py config.json")
