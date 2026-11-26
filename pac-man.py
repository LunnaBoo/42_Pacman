import sys

if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)
    if argc == 2:
        try:
            # to-do: quando arquivo nao existir ou nao tiver permissao
            # logar erro e fechar o programa
            path = argv[1]
            if not argv[1]:
                raise FileNotFoundError("FILE DOESNT EXIST")
            if not argv[1].endswith(".json"):
                raise ValueError("Must be a .json file.")
            from src.ConfigParser import ConfigParser
            config = ConfigParser.from_file(argv[1])
            print(f"Lives: {config.lives}")
            print(f"Highscore file: {config.highscore_filename}")
            print(f"Levels: {len(config.levels)}")
            print(f"Seed: {config.seed}")
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\nError: expected exactly one configuration file."
              "\nUsage: python3 pac-man.py config.json")
