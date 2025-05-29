import argparse
import os


SUBDIRS = ["enum", "exploits", "gobuster", "gold", "tools"]


def create_structure(names):
    for name in names:
        for sub in SUBDIRS:
            path = os.path.join(name, sub)
            os.makedirs(path, exist_ok=True)
        print(f"Created {name} with subdirectories: {', '.join(SUBDIRS)}")


def main():
    parser = argparse.ArgumentParser(
        description="Create directories with enumeration subdirectories",
        add_help=False
    )
    parser.add_argument('-d', dest='dirs', nargs='+', required=True,
                        help='List of directories to create')
    parser.add_argument('-H', '--help', action='help', default=argparse.SUPPRESS,
                        help='show this help message and exit')
    args = parser.parse_args()

    create_structure(args.dirs)


if __name__ == '__main__':
    main()
